"""
Pulls bitcoin price and sentiment data from alpha vantage
"""
from alpha_strategy_api import api_ping, clean_data
import pandas as pd
import requests

'''
grabs the historical price of bitcoin over time and writes it to a csv and returns a df
'''
def get_bitcoin_price_data(symbol):
    function_ = "TIME_SERIES_DAILY"
    data = api_ping(function=function_, symbol=symbol)
    
    '''
    check if time series daily is in data then filter for that data to get daily data
    '''
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]

        dates = []
        close_prices = []

        '''
        Iterate through the daily_data dictionary
        '''
        for date, data in daily_data.items():
            '''
            Extract the date and close price
            '''
            date_obj = pd.to_datetime(date)
            close_price = float(data['4. close'])
            
            '''
            Append to the lists
            '''
            dates.append(date_obj)
            close_prices.append(close_price)

        '''
        Create a DataFrame with Date and Close Price columns
        '''
        df = pd.DataFrame({'Date': dates, 'Close Price': close_prices})

        file_name = 'data/bitcoin_daily_close.csv'
        df.to_csv(file_name, index=False)
        clean_data(df=df, filename=file_name)
        return df
    else:
        return None

'''
Function to retrieve Bitcoin news sentiment data from Alpha Vantage
'''
def get_bitcoin_news_sentiment(symbol):
    '''
    pings alpha vantage api to grab news sentiment data for bitcoin
    '''
    function_ = "NEWS_SENTIMENT"
    data = api_ping(function=function_, symbol=symbol)
    '''
    check if feed is in data then filter for feed data
    '''
    if "feed" in data:
        feed_data = data["feed"]        
        sentiment_scores = []
        '''
        for each item in the feed append its overall sentiment score
        '''
        for item in feed_data:
            overall_sentiment_score = item.get("overall_sentiment_score", 0)
            sentiment_scores.append(overall_sentiment_score)
        
        df = pd.DataFrame(sentiment_scores, columns=["Overall Sentiment Score"])
        file_name = 'data/bitcoin_sentiment.csv'
        df.to_csv(file_name, index=False)
        clean_data(df=df, filename=file_name)
        return df
    else:
        return None

if __name__ == "__main__":
    symbol = "BTCUSD"
    bitcoin_price_data = get_bitcoin_price_data(symbol=symbol)
    
    bitcoin_sentiment_data = get_bitcoin_news_sentiment(symbol=symbol)
    print(bitcoin_price_data)
    print(bitcoin_sentiment_data)