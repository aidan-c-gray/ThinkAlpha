import unittest
from unittest.mock import patch, Mock
import pandas as pd
from src/alpha_strategy_bitcoin.py import get_bitcoin_price_data, get_bitcoin_news_sentiment

class TestBitcoinFunctions(unittest.TestCase):

    @patch('alpha_strategy_api.api_ping')
    def test_get_bitcoin_price_data(self, mock_api_ping):
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
        self.assertTrue(isinstance(bitcoin_price_data, pd.DataFrame))
        self.assertEqual(bitcoin_price_data.shape, (2, 5))
        self.assertAlmostEqual(bitcoin_price_data.iloc[0]['Close'], 30500.00)
        self.assertAlmostEqual(bitcoin_price_data.iloc[1]['Close'], 31800.00)

    @patch('alpha_strategy_api.api_ping')
    def test_get_bitcoin_news_sentiment(self, mock_api_ping):
        # Mock API response
        mock_api_ping.return_value = {
            "sentiment": {
                "positive": 3,
                "neutral": 2,
                "negative": 1
            }
        }

        # Call the function
        bitcoin_sentiment_data = get_bitcoin_news_sentiment("BTCUSD")

        # Check if data is correctly parsed
        self.assertTrue(isinstance(bitcoin_sentiment_data, pd.DataFrame))
        self.assertEqual(bitcoin_sentiment_data.shape, (1, 3))
        self.assertEqual(bitcoin_sentiment_data.loc[0, 'positive'], 3)
        self.assertEqual(bitcoin_sentiment_data.loc[0, 'neutral'], 2)
        self.assertEqual(bitcoin_sentiment_data.loc[0, 'negative'], 1)

if __name__ == "__main__":
    unittest.main()
