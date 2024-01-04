''''
test_alpha_strategy_bitcoin.py

This module contains unit tests for the alpha_strategy_bitcoin module.
'''

from unittest.mock import patch, Mock
from src.alpha_strategy_bitcoin import get_bitcoin_price_data, get_bitcoin_news_sentiment

@patch('src.alpha_strategy_bitcoin.api_ping')
def test_get_bitcoin_price_data(mock_api_ping):
    ''''
    Test the get_bitcoin_price_data function.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks getting Bitcoin price data and checks if the function returns the expected DataFrame.
    '''
    mock_api_response = {
        "Time Series (Daily)": {
            "2023-01-01": {"4. close": "50000.00"},
            "2023-01-02": {"4. close": "52000.00"},
        }
    }
    mock_api_ping.return_value = mock_api_response

    symbol = "BTCUSD"
    df = get_bitcoin_price_data(symbol)  

    assert df is not None
    assert not df.empty
    assert "Date" in df.columns
    assert "Close Price" in df.columns

@patch('src.alpha_strategy_bitcoin.api_ping')
def test_get_bitcoin_price_data_invalid(mock_api_ping):
    ''''
    Test the get_bitcoin_price_data function with an invalid symbol.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks an invalid API response and checks if the function handles it correctly.
    '''
    mock_api_ping.return_value = {"Error Message": "Invalid symbol"}

    symbol = "INVALID_SYMBOL"
    df = get_bitcoin_price_data(symbol)  

    assert df is None

@patch('src.alpha_strategy_bitcoin.api_ping')
def test_get_bitcoin_news_sentiment(mock_api_ping):
    ''''
    Test the get_bitcoin_news_sentiment function.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks getting Bitcoin news sentiment data and checks if the function returns the expected DataFrame.
    '''
    mock_api_response = {
        "feed": [
            {"overall_sentiment_score": 0.75},
            {"overall_sentiment_score": 0.60},
        ]
    }
    mock_api_ping.return_value = mock_api_response

    symbol = "BTCUSD"
    df = get_bitcoin_news_sentiment(symbol)  

    assert df is not None
    assert not df.empty
    assert "Overall Sentiment Score" in df.columns

@patch('src.alpha_strategy_bitcoin.api_ping')
def test_get_bitcoin_news_sentiment_invalid(mock_api_ping):
    ''''
    Test the get_bitcoin_news_sentiment function with an invalid symbol.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks an invalid API response for news sentiment data and checks if the function handles it correctly.
    '''
    mock_api_ping.return_value = {"Error Message": "Invalid symbol"}

    symbol = "INVALID_SYMBOL"
    df = get_bitcoin_news_sentiment(symbol)  

    assert df is None
