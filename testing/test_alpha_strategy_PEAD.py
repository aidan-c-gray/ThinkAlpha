from unittest.mock import patch
from src.alpha_strategy_PEAD import (
    get_small_cap_value,
    get_earnings_data,
    get_small_cap_earnings_data,
    calculate_earnings_drift,
)
def test_get_small_cap_value():
    expected = ["AMR", "MO", "AMCX", "AMN", "ARCT"]  # Include all symbols
    with patch.object(alpha_strategy_api, 'api_ping', return_value=None):
        assert get_small_cap_value() == expected

def test_get_earnings_data():
    mock_api_ping = patch.object(alpha_strategy_api, 'api_ping', return_value={
        "symbol": "AMR",
        "quarterlyEarnings": [{"fiscalDateEnding": "2024-01-01", "reportedEPS": "1.5"}]
    })
    
    with mock_api_ping as mock:
        result = get_earnings_data("AMR")
        
    assert result is not None
    assert isinstance(result, pd.DataFrame)

def test_get_small_cap_earnings_data():
    mock_api_ping = patch.object(alpha_strategy_api, 'api_ping', return_value={
        "symbol": "AMR",
        "quarterlyEarnings": [{"fiscalDateEnding": "2024-01-01", "reportedEPS": "1.5"}]
    })
    
    with mock_api_ping as mock:
        result = get_small_cap_earnings_data()
        
    assert isinstance(result, dict)
    assert "AMR" in result

def test_calculate_earnings_drift():
    df = pd.DataFrame([{"reportedEPS": "2.0"}])
    result = calculate_earnings_drift(df)
    # Assert based on logic in calculate_earnings_drift
