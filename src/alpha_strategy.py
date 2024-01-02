# src/alpha_strategy.py
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup

# AlphaVantage API Key (You can get one by signing up on their website)
api_key = 'IJAW4T1JRMN8CQ9Z'

def api_ping(function, symbol):
    if symbol == "MOM":
            url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=daily&time_period=10&series_type=close&apikey={api_key}'
    else:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json
    return data

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


# Function to retrieve momentum data for a given symbol
def get_momentum_data(symbol):
    function_ = "MOM"
    data = api_ping(function=function_, symbol=symbol)



# Function to calculate earnings drift
def calculate_earnings_drift(earnings_df):
    if earnings_df is None or earnings_df.empty:
        return None

    # Convert 'reportedEPS' column to numeric (float)
    earnings_df["reportedEPS"] = pd.to_numeric(earnings_df["reportedEPS"], errors='coerce')

    # Calculate drift as the difference between the closing price before and after earnings
    earnings_df["Earnings_Drift"] = earnings_df["reportedEPS"] - earnings_df["reportedEPS"].shift(1)

    return earnings_df

if __name__ == "__main__":
    symbol = "AAPL"  # Replace with the symbol of the company you want to analyze
    earnings_data = get_earnings_data(symbol)
    earnings_drift = calculate_earnings_drift(earnings_data)

    if earnings_drift is not None:
        print(earnings_drift)
