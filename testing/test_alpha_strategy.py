# testing/test_alpha_strategy.py
from src.alpha_strategy import get_earnings_data, calculate_earnings_drift, get_close_data
from unittest.mock import patch, Mock
import pandas as pd

def test_get_earnings_data():
    # Test 1: Check if the symbol is not null
    symbol = "AAPL"
    result_df = get_earnings_data(symbol)
    assert symbol is not None

    # Test 2: Check if data is loaded after response.json() call
    assert result_df is not None

    # Test 3: Check if the returned DataFrame is not null
    assert isinstance(result_df, pd.DataFrame)

    # Test 4: Mocking response with no 'quarterlyEarnings' field
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = {}
        result_df = get_earnings_data("AAPL")
        assert result_df is None

    # Test 5: Mocking response with valid 'quarterlyEarnings' field
    earnings_data = {
        "quarterlyEarnings": [
            {"fiscalDateEnding": "2023-09-30", "reportedEPS": "1.46"},
            {"fiscalDateEnding": "2023-06-30", "reportedEPS": "1.26"},
        ]
    }
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = earnings_data
        result_df = get_earnings_data("AAPL")
        assert isinstance(result_df, pd.DataFrame)

    # Test 6: Mocking response with a network error
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network Error")
        result_df = get_earnings_data("AAPL")
        assert result_df is None

def test_calculate_earnings_drift():
    # Add test cases for calculate_earnings_drift function
    pass

def test_get_close_data():
    #Add test cases for get_close_data()
    pass