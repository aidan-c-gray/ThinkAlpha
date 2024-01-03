
import pytest
from unittest.mock import patch
from src.alpha_strategy_api import api_ping

# Mock API key for testing
api_key = "your_test_api_key"

@pytest.mark.parametrize("function, symbol, expected_url", [
    ("MOM", "AAPL", "https://www.alphavantage.co/query?function=MOM&symbol=AAPL&interval=daily&time_period=10&series_type=close&apikey=your_test_api_key"),
    ("TIME_SERIES_DAILY", "MSFT", "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=your_test_api_key"),
    ("NEWS_SENTIMENT", "GOOGL", "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=GOOGL&limit=1000&apikey=your_test_api_key"),
    ("INVALID_FUNCTION", "TSLA", "https://www.alphavantage.co/query?function=INVALID_FUNCTION&symbol=TSLA&apikey=your_test_api_key"),
])
@patch('your_module.requests.get')
def test_api_ping(mock_requests_get, function, symbol, expected_url):
    # Mock the response
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"sample_data": "123"}

    # Call the function
    result = api_ping(function, symbol)

    # Check if the correct URL was constructed
    mock_requests_get.assert_called_once_with(expected_url)

    # Check if the API request was successful
    assert result == {"sample_data": "123"}

@patch('your_module.requests.get')
def test_api_ping_error(mock_requests_get):
    # Mock an error response
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 500

    # Call the function
    result = api_ping("MOM", "AAPL")

    # Check if the API request failed and returned None
    assert result is None
