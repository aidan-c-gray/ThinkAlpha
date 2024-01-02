from alpha_strategy_api import api_ping, get_stock_price_data
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
    print(data)
    if "quarterlyEarnings" in data:
        ticker = data["symbol"]
        earnings = data["quarterlyEarnings"]
        df = pd.DataFrame(earnings)
        df['ticker'] = ticker
        df = df[['fiscalDateEnding', 'reportedDate', 'ticker', 'reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']]
        return df
    else:
        return None

def get_small_cap_earnings_data():
    small_cap_value = get_small_cap_value()
    data_dict = {}
    combined_df = pd.DataFrame()
    for item in small_cap_value:
        df = get_earnings_data(item)
        if df is not None:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            data_dict[item] = (df[['fiscalDateEnding', 'reportedDate', 'reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']])
    file_name = 'data/earnings_tech.csv'
    combined_df.to_csv(file_name, index=False)
    return data_dict
        
def get_small_cap_close_data():
    small_cap_value = get_small_cap_value()
    for item in small_cap_value:
        get_stock_price_data(item)
        

# Function to calculate earnings drift
def calculate_earnings_drift(earnings_df):
    if earnings_df is None or earnings_df.empty:
        return None

    earnings_df["reportedEPS"] = pd.to_numeric(earnings_df["reportedEPS"], errors='coerce')

    # Calculate drift as the difference between the closing price before and after earnings
    return earnings_df


if __name__ == "__main__":
    # get_small_cap_close_data()
    get_small_cap_earnings_data()