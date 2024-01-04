import os
import secrets
import pandas as pd
import requests
api_key = os.environ.get("API_KEY")
# takes function and symbol and returns data retrieved from alphavantage api
def api_ping(function, symbol):
    if function == "MOM":
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=daily&time_period=10&series_type=close&apikey={api_key}'
    elif function == "TIME_SERIES_DAILY":
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key}'
    elif function == "NEWS_SENTIMENT":
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&limit=1000&apikey={api_key}'
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

def get_stock_price_data(symbol):
    function_ = "TIME_SERIES_DAILY"
    data = api_ping(function=function_, symbol=symbol)
    
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]
    
        # Initialize empty lists to store dates and close prices
        dates = []
        close_prices = []

        # Iterate through the daily_data dictionary
        for date, data in daily_data.items():
            # Extract the date and close price
            date_obj = pd.to_datetime(date)
            close_price = float(data['4. close'])
            
            # Append to the lists
            dates.append(date_obj)
            close_prices.append(close_price)

        # Create a DataFrame with Date and Close Price columns
        df = pd.DataFrame({'Date': dates, 'Close Price': close_prices})

        file_name = f'data/{symbol}_daily_close.csv'
        df.to_csv(file_name, index=False)
        clean_data(df=df, filename=file_name)
        return df
    else:
        return None

def clean_data(df, filename):
    df.dropna(inplace=True)  # Remove rows with any null values
    df.drop_duplicates(inplace=True)  # Remove duplicate rows

    # Save the cleaned DataFrames back to CSV files if needed
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    symbol = "AAPL"  
    print(symbol)
