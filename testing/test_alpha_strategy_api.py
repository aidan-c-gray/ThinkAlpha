''''
test_alpha_strategy_api.py

This module contains unit tests for the alpha_strategy_api module.
'''

import pytest
import requests
from unittest.mock import patch, Mock
from src.alpha_strategy_api import api_ping, get_stock_price_data

@pytest.fixture
def sample_api_key():
    ''''
    Fixture function that returns a sample API key for testing purposes.
    Replace with an actual API key for testing.
    '''
    return "HOZZSE2154NAZOO7"

@patch('src.alpha_strategy_api.requests.get')
def test_api_ping_valid(mock_get, sample_api_key):
    ''''
    Test the api_ping function with a valid API response.

    Args:
        mock_get: A mocked version of the requests.get function.
        sample_api_key: A sample API key for testing.

    This test mocks a valid API response and checks if the function returns the expected response.
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Time Series (Daily)": {"2023-01-01": {"4. close": "150.00"}}}
    mock_get.return_value = mock_response

    function = "TIME_SERIES_DAILY"
    symbol = "AAPL"
    response = api_ping(function, symbol) 

    assert response is not None
    assert "Time Series (Daily)" in response

@patch('src.alpha_strategy_api.requests.get')
def test_api_ping_invalid(mock_get, sample_api_key):
    ''''
    Test the api_ping function with an invalid API response.

    Args:
        mock_get: A mocked version of the requests.get function.
        sample_api_key: A sample API key for testing.

    This test mocks an invalid API response and checks if the function handles it correctly.
    '''
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    function = "TIME_SERIES_DAILY"
    symbol = "INVALID_SYMBOL"
    response = api_ping(function, symbol) 

    assert response is None

@patch('src.alpha_strategy_api.requests.get')
def test_get_stock_price_data(mock_get, sample_api_key):
    ''''
    Test the get_stock_price_data function with a valid symbol.

    Args:
        mock_get: A mocked version of the requests.get function.
        sample_api_key: A sample API key for testing.

    This test mocks getting stock price data and checks if the function returns the expected DataFrame.
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Time Series (Daily)": {"2023-01-01": {"4. close": "150.00"}},
        "Meta Data": {"2. Symbol": "AAPL"}
    }
    mock_get.return_value = mock_response

    symbol = "AAPL"
    df = get_stock_price_data(symbol)  # Remove api_key argument

    assert df is not None
    assert not df.empty
    assert "Date" in df.columns
    assert "Close Price" in df.columns

@patch('src.alpha_strategy_api.requests.get')
def test_get_stock_price_data_invalid_symbol(mock_get, sample_api_key):
    ''''
    Test the get_stock_price_data function with an invalid symbol.

    Args:
        mock_get: A mocked version of the requests.get function.
        sample_api_key: A sample API key for testing.

    This test mocks getting stock price data for an invalid symbol and checks if the function handles it correctly.
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Error Message": "Invalid symbol"}
    mock_get.return_value = mock_response

    symbol = "INVALID_SYMBOL"
    df = get_stock_price_data(symbol)  

    assert df is None
