
import pytest
from src.alpha_strategy_PEAD import get_small_cap_value, get_earnings_data, get_small_cap_earnings_data, calculate_earnings_drift
import pandas as pd

def test_get_small_cap_value():
    expected = ["AMR", "MO", "AMCX", "AMN", "ARCT", ...]  # include all symbols
    assert get_small_cap_value() == expected

def test_get_earnings_data(mocker):
    mock_api_ping = mocker.patch('alpha_strategy_api.api_ping', return_value={
        "symbol": "AMR",
        "quarterlyEarnings": [{"fiscalDateEnding": "2024-01-01", "reportedEPS": "1.5"}]
    })
    result = get_earnings_data("AMR")
    assert result is not None
    assert isinstance(result, pd.DataFrame)

def test_get_small_cap_earnings_data(mocker):
    mock_api_ping = mocker.patch('alpha_strategy_api.api_ping', return_value={
        "symbol": "AMR",
        "quarterlyEarnings": [{"fiscalDateEnding": "2024-01-01", "reportedEPS": "1.5"}]
    })
    result = get_small_cap_earnings_data()
    assert isinstance(result, dict)
    assert "AMR" in result

def test_calculate_earnings_drift():
    df = pd.DataFrame([{"reportedEPS": "2.0"}])
    result = calculate_earnings_drift(df)
    # Assert based on  logic in calculate_earnings_drift

# Note: get_small_cap_close_data test is omitted because it prints output without returning anything
