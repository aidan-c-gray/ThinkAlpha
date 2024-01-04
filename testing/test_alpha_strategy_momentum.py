''''
test_alpha_strategy_momentum.py

This module contains unit tests for the alpha_strategy_momentum module.
'''

from unittest.mock import patch, Mock
from src.alpha_strategy_momentum import get_momentum_data, retrieve_momentum_data_for_tech_stocks

@patch('src.alpha_strategy_momentum.api_ping')
def test_get_momentum_data(mock_api_ping):
    ''''
    Test the get_momentum_data function.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks getting momentum data and checks if the function returns the expected DataFrame.
    '''
    mock_api_response = {
        "Technical Analysis: MOM": {
            "2023-01-01": {"mom_score": "0.75"},
            "2023-01-02": {"mom_score": "0.60"},
        }
    }
    mock_api_ping.return_value = mock_api_response

    symbol = "AAPL"
    df = get_momentum_data(symbol) 

    assert df is not None
    assert not df.empty
    assert "date" in df.columns
    assert "mom_score" in df.columns

@patch('src.alpha_strategy_momentum.api_ping')
def test_get_momentum_data_invalid(mock_api_ping):
    ''''
    Test the get_momentum_data function with an invalid symbol.

    Args:
        mock_api_ping: A mocked version of the api_ping function.

    This test mocks an invalid API response and checks if the function handles it correctly.
    '''
    mock_api_ping.return_value = {"Error Message": "Invalid symbol"}

    symbol = "INVALID_SYMBOL"
    df = get_momentum_data(symbol)  
    assert df is None

@patch('src.alpha_strategy_momentum.get_stock_price_data')
def test_retrieve_momentum_data_for_tech_stocks(mock_get_stock_price_data):
    ''''
    Test the retrieve_momentum_data_for_tech_stocks function.

    Args:
        mock_get_stock_price_data: A mocked version of the get_stock_price_data function.

    This test mocks retrieving momentum data for tech stocks and checks if the function returns the expected data dictionary.
    '''
    mock_df = Mock()
    mock_df.empty = False
    mock_get_stock_price_data.return_value = mock_df

    tech_stocks = ["AAPL", "MSFT"]

    data_dict = retrieve_momentum_data_for_tech_stocks()

    assert data_dict is not None
    assert "AAPL" in data_dict
    assert "MSFT" in data_dict
