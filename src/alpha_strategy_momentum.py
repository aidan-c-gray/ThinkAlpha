from alpha_strategy_api import api_ping
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup

# Function to retrieve the list of largest tech industry stocks
def get_largest_tech_stocks():
    top_tech_stocks = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "TSM", "AVGO", "ASML", "ORCL", "ADBE", "CRM", "AMD", "NFLX", "CSCO", "INTC", "BABA"]
    return top_tech_stocks

# Function to retrieve momentum data for a given symbol/symbols
def get_momentum_data(symbol):
    function_ = "MOM"
    data = api_ping(function=function_, symbol=symbol)
    if "MOM" in data:
        momentum_data = data["MOM"]
        df = pd.DataFrame(momentum_data)
        return df
    else:
        return None

# Function to retrieve momentum data for the largest tech stocks
def retrieve_momentum_data_for_tech_stocks():
    tech_stocks = get_largest_tech_stocks()
    
    momentum_data_dict = {}
    
    for symbol in tech_stocks:
        momentum_data = get_momentum_data(symbol)
        if momentum_data is not None:
            momentum_data_dict[symbol] = momentum_data
    
    return momentum_data_dict