import sys
sys.path.append('/app')
import pytest
from src.alpha_strategy_bitcoin import get_bitcoin_news_sentiment, get_bitcoin_price_data
from unittest.mock import patch
from src.alpha_strategy_bitcoin import get_bitcoin_price_data, get_bitcoin_news_sentiment

@patch('alpha_strategy_api.api_ping')
def test_get_bitcoin_price_data(mock_api_ping):
    # Mock API response
    mock_api_ping.return_value = {
        "Time Series (Daily)": {
            "2023-01-01": {"1. open": "30000.00", "2. high": "31000.00", "3. low": "29000.00", "4. close": "30500.00", "5. volume": "10000"},
            "2023-01-02": {"1. open": "30500.00", "2. high": "32000.00", "3. low": "30200.00", "4. close": "31800.00", "5. volume": "12000"},
        }
    }

    # Call the function
    bitcoin_price_data = get_bitcoin_price_data("BTCUSD")

    # Check if data is correctly parsed
    assert isinstance(bitcoin_price_data, pd.DataFrame)
    assert bitcoin_price_data.shape == (2, 5)
    assert bitcoin_price_data.iloc[0]['Close'] == 30500.00
    assert bitcoin_price_data.iloc[1]['Close'] == 31800.00
print(get_bitcoin_price_data("BTCUSD"))
@patch('alpha_strategy_api.api_ping')
def test_get_bitcoin_news_sentiment(mock_api_ping):
    # Mock API response
    mock_api_ping.return_value = {
        "feed": [
            {
                "overall_sentiment_score": 0.8
            }
        ]
    }

    # Call the function
    bitcoin_sentiment_data = get_bitcoin_news_sentiment("BTCUSD")

    # Check if data is correctly parsed
    assert isinstance(bitcoin_sentiment_data, pd.DataFrame)
    assert bitcoin_sentiment_data.shape == (1, 1)
    assert bitcoin_sentiment_data.loc[0, 'Overall Sentiment Score'] == 0.8
