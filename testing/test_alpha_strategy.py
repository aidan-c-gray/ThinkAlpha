from src.alpha_strategy import get_earnings_data, calculate_earnings_drift, get_close_data
from unittest.mock import patch, Mock
import pandas as pd

# Mock the api_ping function for testing purposes
def mock_api_ping(function, symbol):
    mocked_data = {
        "close": {
            "2023-12-31": "150.00",
            "2023-12-30": "149.50",
            "2023-12-29": "149.75",
        },
        "MOM": {
            "2023-12-31": {"MOM": "2.34"},
            "2023-12-30": {"MOM": "1.98"},
            "2023-12-29": {"MOM": "1.72"},
        },
    }
    return mocked_data.get(function, {})

@pytest.fixture
def mock_api_ping_fixture(monkeypatch):
    monkeypatch.setattr("src.alpha_strategy.api_ping", mock_api_ping)

# Unit tests for earnings data retrieval
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
        
# Unit tests for earnings drift calculations
def test_calculate_earnings_drift():
    earnings_data = {
        "reportedEPS": ["1.46", "1.26", "1.72", "1.98"],
        "fiscalDateEnding": ["2023-09-30", "2023-06-30", "2023-03-31", "2022-12-31"],
    }
    earnings_df = pd.DataFrame(earnings_data)

    # Test 1: Check if earnings drift is calculated correctly
    result_df = calculate_earnings_drift(earnings_df)
    assert isinstance(result_df, pd.DataFrame)
    assert "Earnings_Drift" in result_df.columns
    assert result_df["Earnings_Drift"].equals(pd.Series([None, 0.20, -0.46, 0.26]))

    # Test 2: Check if handling None or empty DataFrame returns None
    assert calculate_earnings_drift(None) is None
    assert calculate_earnings_drift(pd.DataFrame()) is None

# Unit tests for close price data retrieval
def test_get_close_price_data(mock_api_ping_fixture):
    # Test 1: Check if close price data is retrieved successfully
    symbol = "AAPL"
    close_data = get_close_price_data(symbol)
    assert isinstance(close_data, pd.DataFrame)
    assert not close_data.empty

# Unit tests for momentum data retrieval
def test_get_momentum_data(mock_api_ping_fixture):
    # Test 1: Check if momentum data is retrieved successfully
    symbol = "AAPL"
    momentum_data = get_momentum_data(symbol)
    assert isinstance(momentum_data, pd.DataFrame)
    assert not momentum_data.empty

