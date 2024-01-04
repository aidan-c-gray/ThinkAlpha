from unittest.mock import patch, Mock
import pandas as pd
from src.alpha_strategy_PEAD import (
    get_small_cap_value,
    get_earnings_data,
    get_small_cap_earnings_data,
    get_small_cap_close_data,
    calc_earnings_drift,
)

# Test get_earnings_data
@patch('src.alpha_strategy_PEAD.api_ping')
def test_get_earnings_data(mock_api_ping):
    # Mock the api_ping function for earnings data
    mock_api_response = {
        "quarterlyEarnings": [
            {
                "fiscalDateEnding": "2023-09-30",
                "reportedDate": "2023-11-02",
                "ticker": "AMR",
                "reportedEPS": 6.65,
                "estimatedEPS": 6.46,
                "surprise": 0.19,
                "surprisePercentage": 2.9412,
            }
        ],
        "symbol": "AMR",
    }
    mock_api_ping.return_value = mock_api_response

    symbol = "AMR"
    df = get_earnings_data(symbol)

    expected_columns = [
        "fiscalDateEnding", "reportedDate", "ticker",
        "reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"
    ]

    assert df is not None
    assert df.columns.tolist() == expected_columns
    assert len(df) == 1
    assert df.iloc[0]["ticker"] == symbol

# Test get_earnings_data with invalid symbol
@patch('src.alpha_strategy_PEAD.api_ping')
def test_get_earnings_data_invalid(mock_api_ping):
    # Mock an invalid API response for earnings data
    mock_api_ping.return_value = {"Error Message": "Invalid symbol"}

    symbol = "INVALID_SYMBOL"
    df = get_earnings_data(symbol)

    assert df is None

# Test get_small_cap_value
def test_get_small_cap_value():
    small_cap_value = get_small_cap_value()
    expected_stocks = [
        "AMR", "MO", "AMCX", "AMN", "ARCT", "ARHS", "BKE", "BBW", "CPRX", "LNG",
        "COLL", "CCSI", "CROX", "CVI", "EVRI", "FOXA", "GTX", "GCT", "GPOR",
        "HRB", "HRMY", "HSII", "HPQ", "IDCC", "IPG", "IRWD", "JILL", "JAKK",
        "LSXMK", "MBUU", "MCFT", "MED", "MLI", "NATH", "OMC", "PARR", "MD",
        "PRDO", "PLTK", "PINC", "RGP", "RMNI", "SMLR", "STGW", "TH", "UIS",
        "UNTC", "VGR", "VYGR", "ZYME"
    ]
    assert sorted(small_cap_value) == sorted(expected_stocks)

# Test get_small_cap_earnings_data
@patch('src.alpha_strategy_PEAD.get_earnings_data')
def test_get_small_cap_earnings_data(mock_get_earnings_data):
    # Mock the get_earnings_data function to return a DataFrame
    mock_df = pd.DataFrame({
        'fiscalDateEnding': ['2023-09-30'],
        'reportedDate': ['2023-11-02'],
        'ticker': ['AMR'],
        'reportedEPS': [6.65],
        'estimatedEPS': [6.46],
        'surprise': [0.19],
        'surprisePercentage': [2.9412]
    })
    mock_get_earnings_data.return_value = mock_df

    small_cap_stocks = get_small_cap_value()
    data_dict = get_small_cap_earnings_data()

    assert data_dict is not None
    for stock in small_cap_stocks:
        assert stock in data_dict


# Test get_small_cap_close_data
@patch('src.alpha_strategy_PEAD.get_stock_price_data')
def test_get_small_cap_close_data(mock_get_stock_price_data):
    # Mock the get_stock_price_data function
    mock_get_stock_price_data.return_value = None

    small_cap_stocks = get_small_cap_value()
    get_small_cap_close_data()

    # Ensure get_stock_price_data was called for each stock
    assert mock_get_stock_price_data.call_count == len(small_cap_stocks)

# Test calc_earnings_drift
@patch('src.alpha_strategy_PEAD.os.path.exists')
@patch('src.alpha_strategy_PEAD.calc_earnings_drift')
@patch('src.alpha_strategy_PEAD.pd.read_csv')
def test_calc_earnings_drift(mock_read_csv, mock_calc_earnings_drift, mock_path_exists):
    mock_path_exists.return_value = True
    
    # Modify the DataFrame to include a "ticker" column
    mock_read_csv.side_effect = [
        pd.DataFrame({'Date': ['2023-01-01', '2023-01-02'], 'Price': [100.0, 105.0]}),
        pd.DataFrame({'Date': ['2023-01-01', '2023-01-02'], 'Price': [100.0, 105.0], 'ticker': ['AMR', 'AMR']}),  # Include "ticker" column
    ]
    
    # Ensure that the calc_earnings_drift function is called
    calc_earnings_drift()

    # Ensure the relevant functions are called
    assert mock_path_exists.called
    assert mock_read_csv.call_count == 2
    mock_calc_earnings_drift.assert_called_once()

