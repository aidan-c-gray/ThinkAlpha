import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup

# Personal free API key
api_key = '9EQWTW3JJFKP8BLY'

# takes function and symbol and returns data retrieved from alphavantage api
def api_ping(function, symbol):
    if function == "MOM":
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=daily&time_period=10&series_type=close&apikey={api_key}'
    elif function == "TIME_SERIES_DAILY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}'
    else:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    
    # Check if the API request was successful
    if response.status_code == 200:
        data = response.json()  # Corrected to call the json() method
        return data
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None


if __name__ == "__main__":
    symbol = "AAPL"  
    print(symbol)
