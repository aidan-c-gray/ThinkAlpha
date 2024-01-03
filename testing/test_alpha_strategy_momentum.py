from src.alpha_strategy_momentum import get_largest_tech_stocks, get_momentum_data, retrieve_momentum_data_for_tech_stocks, get_tech_sector_data

def test_get_largest_tech_stocks():
    expected = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "TSM", "AVGO", "ASML", "ORCL", "ADBE", "CRM", "AMD", "NFLX", "CSCO", "INTC", "BABA"]
    assert get_largest_tech_stocks() == expected

def test_get_momentum_data(mocker):
    mock_api_ping = mocker.patch('src.alpha_strategy_api.api_ping', return_value={"Technical Analysis: MOM": {"2024-01-01": {"MOM": "5.0"}}})
    result = get_momentum_data("AAPL")
    assert result is not None
    assert isinstance(result, pd.DataFrame)

def test_retrieve_momentum_data_for_tech_stocks(mocker):
    mock_api_ping = mocker.patch('src.alpha_strategy_api.api_ping', return_value={"Technical Analysis: MOM": {"2024-01-01": {"MOM": "5.0"}}})
    result = retrieve_momentum_data_for_tech_stocks()
    assert isinstance(result, dict)
    assert "AAPL" in result

def test_get_tech_sector_data(mocker):
    mocker.patch('src.alpha_strategy_api.get_stock_price_data', return_value={"Price": "150"})
    # You may want to check for output or side effects here
    get_tech_sector_data()
