from alpha_strategy_api import api_ping
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup

# Function to retrieve the list of value stocks greater than 250M MC filtered for yield and p/e
def get_small_cap_value():
    small_cap_value = ["AMR", "MO", "AMCX", "AMN", "ARCT", "ARHS", "BKE", "BBW", "CPRX", "LNG", "COLL", "CCSI", "CROX", "CVI", "EVRI", "FOXA", "GTX", "GCT", "GPOR", "HRB", "HRMY", "HSII", "HPQ", "IDCC", "IPG", "IRWD", "JILL", "JAKK", "LSXMK", "MBUU", "MCFT", "MED", "MLI", "NATH", "OMC", "PARR", "MD", "PRDO", "PLTK", "PINC", "RGP", "RMNI", "SMLR", "STGW", "TH", "UIS", "UNTC", "VGR", "VYGR", "ZYME"]
    return small_cap_value

# Function to retrieve earnings data for a given symbol
def get_earnings_data(symbol):
    function_ = "EARNINGS"
    data = api_ping(function=function_, symbol=symbol)
    if "quarterlyEarnings" in data:
        earnings = data["quarterlyEarnings"]
        df = pd.DataFrame(earnings)
        return df
    else:
        return None
    
# Function to retrieve close data for a given symbol
def get_close_price_data(symbol):
    function_ = "TIME_SERIES_DAILY"
    data = api_ping(function=function_, symbol=symbol)
    if "close" in data:
        close = data["close"]
        df = pd.DataFrame(close)
        return df
    else:
        None


# Function to calculate earnings drift
def calculate_earnings_drift(earnings_df):
    if earnings_df is None or earnings_df.empty:
        return None

    earnings_df["reportedEPS"] = pd.to_numeric(earnings_df["reportedEPS"], errors='coerce')

    # Calculate drift as the difference between the closing price before and after earnings

    return earnings_df