from alpha_strategy_api import api_ping
import pandas as pd
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt

def get_bitcoin_price_data(symbol):
    function_ = "TIME_SERIES_DAILY"
    data = api_ping(function=function_, symbol = symbol)
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(daily_data, orient='index', columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        df.index = pd.to_datetime(df.index)
        df = df.astype({'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int})
        return df
    else:
        return None

# Function to retrieve Bitcoin news sentiment data from Alpha Vantage
def get_bitcoin_news_sentiment(symbol):
    function_ = "NEWS_SENTIMENT"
    data = api_ping(function=function_, symbol=symbol)
    print(data)
    if "sentiment" in data:
        sentiment_data = data["sentiment"]
        df = pd.DataFrame(sentiment_data, index=[0])
        return df
    else:
        return None
    
if __name__ == "__main__":
    symbol = "BTCUSD"
    # Retrieve Bitcoin price data
    bitcoin_price_data = get_bitcoin_price_data(symbol=symbol)
    
    # Retrieve Bitcoin news sentiment data
    bitcoin_sentiment_data = get_bitcoin_news_sentiment(symbol=symbol)
    
    # Plot Bitcoin price and sentiment data
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    
    ax1.plot(bitcoin_price_data.index, bitcoin_price_data['Close'], color='b', label='Bitcoin Price (USD)')
    ax2.plot(bitcoin_sentiment_data.columns, bitcoin_sentiment_data.values[0], color='r', label='Sentiment Score')
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Bitcoin Price (USD)', color='b')
    ax2.set_ylabel('Sentiment Score', color='r')
    
    plt.title('Bitcoin Price and News Sentiment')
    plt.legend()
    plt.show()