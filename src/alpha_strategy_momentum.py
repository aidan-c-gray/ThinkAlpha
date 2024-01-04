'''
collects data to be used for momentum strategy from alpha vantage. Stocks used are a subset of the largest
tech stocks
'''
from .alpha_strategy_api import api_ping, get_stock_price_data, clean_data
import os
import pandas as pd

'''
Function to retrieve the list of largest tech industry stocks
'''
def get_largest_tech_stocks():
    top_tech_stocks = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "TSM", "AVGO", "ASML", "ORCL", "ADBE", "CRM", "AMD", "NFLX", "CSCO", "INTC", "BABA"]
    return top_tech_stocks

'''
Function to retrieve momentum data for a given symbol/stock
'''
def get_momentum_data(symbol):
    function_ = "MOM"
    data = api_ping(function=function_, symbol=symbol)
    if "Technical Analysis: MOM" in data:
        momentum_data = data["Technical Analysis: MOM"]
        
        '''
        Convert the dictionary to a DataFrame
        '''
        df = pd.DataFrame.from_dict(momentum_data, orient='index')
        df = df.reset_index()
        df.columns = ['date', 'mom_score']
        
        '''
        Add a 'ticker' column with the symbol
        '''
        df['ticker'] = symbol
        
        return df
    else:
        return None

'''
Function to retrieve momentum data for the largest tech stocks 
'''
def retrieve_momentum_data_for_tech_stocks():
    tech_stocks = get_largest_tech_stocks()
    
    data_dict = {}
    combined_df = pd.DataFrame()

    '''
    iterates through tech stocks calling get_momentum_data for each stock creating a combined csv
    of momentum scores
    '''
    for symbol in tech_stocks:
        df = get_momentum_data(symbol)
        if df is not None:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            data_dict[symbol] = (df[['date', 'mom_score']])
    file_name = 'data/momentum_tech.csv'
    combined_df.to_csv(file_name, index=False)
    clean_data(df=combined_df, filename='data/earnings_momentum.csv')
    return data_dict

'''
calls function whcih retrieves stock price data for every stock in largest tech stocks
'''
def get_tech_sector_data():
    tech_stocks = get_largest_tech_stocks()
    for item in tech_stocks:
        test= get_stock_price_data(item)
        print(test)
        


if __name__ == "__main__":
    get_largest_tech_stocks()
    # momentum = retrieve_momentum_data_for_tech_stocks()
    # momentum_aapl = momentum["AAPL"]
    # print(momentum_aapl[momentum_aapl["date"] == '2023-12-07']['mom_score'])
    # get_tech_sector_data()