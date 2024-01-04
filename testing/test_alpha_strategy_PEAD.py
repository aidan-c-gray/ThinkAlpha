''''
test_alpha_strategy_PEAD.py

This module contains unit tests for the alpha_strategy_PEAD module.
'''

from unittest.mock import patch, Mock
import pandas as pd
from src.alpha_strategy_PEAD import (
    get_small_cap_value,
    get_earnings_data,
    get_small_cap_earnings_data,
    get_small_cap_close_data,
    calc_earnings_drift,
)

@patch('src.alpha_strategy_PEAD.api_ping')
def test_get_earnings_data(mock_api_ping):
    ''''
    Test the get_earnings_data function.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks getting earnings data and checks if the function returns the expected DataFrame.
    '''
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

@patch('src.alpha_strategy_PEAD.api_ping')
def test_get_earnings_data_invalid(mock_api_ping):
    ''''
    Test the get_earnings_data function with an invalid symbol.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks an invalid API response and checks if the function handles it correctly.
    '''
    mock_api_ping.return_value = {"Error Message": "Invalid symbol"}

    symbol = "INVALID_SYMBOL"
    df = get_earnings_data(symbol)

    assert df is None

def test_get_small_cap_value():
    ''''
    Test the get_small_cap_value function.

    This test checks if the function returns the expected list of small-cap value stocks.
    '''
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

@patch('src.alpha_strategy_PEAD.get_earnings_data')
def test_get_small_cap_earnings_data(mock_get_earnings_data):
    ''''
    Test the get_small_cap_earnings_data function.

    Args:
        mock_get_earnings_data: A mocked version of the get_earnings_data function.

    This test mocks getting earnings data for small-cap value stocks and checks if the function returns the expected data dictionary.
    '''
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


@patch('src.alpha_strategy_PEAD.get_stock_price_data')
def test_get_small_cap_close_data(mock_get_stock_price_data):
    ''''
    Test the get_small_cap_close_data function.

    Args:
        mock_get_stock_price_data: A mocked version of the get_stock_price_data function.

    This test mocks getting close price data for small-cap value stocks and checks if the function calls the expected number of times.
    '''
    mock_get_stock_price_data.return_value = None

    small_cap_stocks = get_small_cap_value()
    get_small_cap_close_data()

   
