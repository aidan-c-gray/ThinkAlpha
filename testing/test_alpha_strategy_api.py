from unittest.mock import patch, MagicMock
import pytest
from src.alpha_strategy_api import api_ping, get_stock_price_data
import os

# Function to manually load environment variables from a file
def load_env(file_path):
    with open(file_path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Load environment variables
load_env('secrets.env')


@pytest.mark.parametrize("function, symbol, expected_url", [
    ("MOM", "AAPL", "https://www.alphavantage.co/query?function=MOM&symbol=AAPL&interval=daily&time_period=10&series_type=close&apikey=test_api_key"),
    # Add more test cases for different functions and symbols
])
@patch('your_module.requests.get')
def test_api_ping(mock_get, function, symbol, expected_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    result = api_ping(function, symbol)
    mock_get.assert_called_once_with(expected_url)
    assert result == {"data": "test"}

@patch('your_module.api_ping')
def test_get_stock_price_data(mock_api_ping):
    mock_api_ping.return_value = {
        "Time Series (Daily)": {
            "2021-01-01": {"4. close": "100.00"},
            "2021-01-02": {"4. close": "101.00"},
        }
    }
    result = get_stock_price_data("AAPL")
    assert isinstance(result, pd.DataFrame)
    assert result.iloc[0]['Close Price'] == 100.00
    assert result.iloc[1]['Close Price'] == 101.00
