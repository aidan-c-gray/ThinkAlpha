# tests/test_alpha_strategy_api.py

import pytest
import requests
from unittest.mock import patch, Mock
from src.alpha_strategy_api import api_ping, get_stock_price_data

@pytest.fixture
def sample_api_key():
    return "HOZZSE2154NAZOO7"  # Replace with an actual API key for testing

@patch('src.alpha_strategy_api.requests.get')
def test_api_ping_valid(mock_get, sample_api_key):
    # Mock a valid API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Time Series (Daily)": {"2023-01-01": {"4. close": "150.00"}}}
    mock_get.return_value = mock_response

    function = "TIME_SERIES_DAILY"
    symbol = "AAPL"
    # The api_key should be handled within the api_ping function
    response = api_ping(function, symbol)  # Remove api_key argument

    assert response is not None
    assert "Time Series (Daily)" in response

@patch('src.alpha_strategy_api.requests.get')
def test_api_ping_invalid(mock_get, sample_api_key):
    # Mock an invalid API response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    function = "TIME_SERIES_DAILY"
    symbol = "INVALID_SYMBOL"
    # The api_key should be handled within the api_ping function
    response = api_ping(function, symbol)  # Remove api_key argument

    assert response is None

@patch('src.alpha_strategy_api.requests.get')
def test_get_stock_price_data(mock_get, sample_api_key):
    # Mock getting stock price data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Time Series (Daily)": {"2023-01-01": {"4. close": "150.00"}},
        "Meta Data": {"2. Symbol": "AAPL"}
    }
    mock_get.return_value = mock_response

    symbol = "AAPL"
    # The api_key should be handled within the get_stock_price_data function
    df = get_stock_price_data(symbol)  # Remove api_key argument

    assert df is not None
    assert not df.empty
    assert "Date" in df.columns
    assert "Close Price" in df.columns

@patch('src.alpha_strategy_api.requests.get')
def test_get_stock_price_data_invalid_symbol(mock_get, sample_api_key):
    # Mock getting stock price data for an invalid symbol
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Error Message": "Invalid symbol"}
    mock_get.return_value = mock_response

    symbol = "INVALID_SYMBOL"
    # The api_key should be handled within the get_stock_price_data function
    df = get_stock_price_data(symbol)  # Remove api_key argument

    assert df is None
