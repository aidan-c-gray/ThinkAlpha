'''
grabs the historical price data for every small cap value stock listed below as well as the quarterly earnings 
of each company. Then calcuates the earnings drift for each earnings report
'''
from alpha_strategy_api import api_ping, get_stock_price_data, clean_data
import os
import pandas as pd
from datetime import datetime, timedelta

'''
Function to retrieve the list of value stocks greater than 250M MC filtered for yield and p/e
'''
def get_small_cap_value():
    small_cap_value = ["AMR", "MO", "AMCX", "AMN", "ARCT", "ARHS", "BKE", "BBW", "CPRX", "LNG", "COLL", "CCSI", "CROX", "CVI", "EVRI", "FOXA", "GTX", "GCT", "GPOR", "HRB", "HRMY", "HSII", "HPQ", "IDCC", "IPG", "IRWD", "JILL", "JAKK", "LSXMK", "MBUU", "MCFT", "MED", "MLI", "NATH", "OMC", "PARR", "MD", "PRDO", "PLTK", "PINC", "RGP", "RMNI", "SMLR", "STGW", "TH", "UIS", "UNTC", "VGR", "VYGR", "ZYME"]
    return small_cap_value

'''
Function to retrieve earnings data for a given symbol and store it in a data frame
'''
def get_earnings_data(symbol):
    function_ = "EARNINGS"
    data = api_ping(function=function_, symbol=symbol)
    if "quarterlyEarnings" in data:
        ticker = data["symbol"]
        earnings = data["quarterlyEarnings"]
        df = pd.DataFrame(earnings)
        df['ticker'] = ticker
        df = df[['fiscalDateEnding', 'reportedDate', 'ticker', 'reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']]
        return df
    else:
        return None

'''
Function to get the small cap earnings data. Consist of adding all earnings data for every company to one
large dataframe
'''
def get_small_cap_earnings_data():
    '''
    iterates over every small cap stock and get earnings data for given stock and ad it to the combined
    dataframe
    '''
    small_cap_value = get_small_cap_value()
    data_dict = {}
    combined_df = pd.DataFrame()
    for item in small_cap_value:
        df = get_earnings_data(item)
        if df is not None:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            data_dict[item] = (df[['fiscalDateEnding', 'reportedDate', 'reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']])
    '''
    writes to data to a csv
    '''
    file_name = 'data/earnings_tech.csv'
    combined_df.to_csv(file_name, index=False)
    clean_data(df=combined_df, filename='data/earnings_tech.csv')
    return data_dict
        
'''
gets the historical price data for all small cap value stocks listed
'''  
def get_small_cap_close_data():
    small_cap_value = get_small_cap_value()
    for item in small_cap_value:
        get_stock_price_data(item)
        
'''
calculates the earnings drift for 75 days post report date
'''
def calc_earnings_drift():
    earnings_df = pd.read_csv('data/earnings_tech.csv')
    combined_data = []
    time_window = 75
    earnings_df = earnings_df.dropna()

    '''
    iterates over earnings df
    '''
    for index, row in earnings_df.iterrows():
        ticker = row["ticker"]
        reported_date = datetime.strptime(row["reportedDate"], "%Y-%m-%d")
        surprise_percentage = row["surprisePercentage"]
        '''
        Check if the price data file for the stock exists
        '''
        price_data_file = f'data/{ticker}_daily_close.csv'

        if os.path.exists(price_data_file):
            '''
            Load the price data for the stock
            '''
            price_df = pd.read_csv(price_data_file, parse_dates=["Date"])

            '''Filter price data for dates within the time window
            start_index = price_df[price_df["Date"] > reported_date].index[price_df[price_df["Date"] > reported_date].count()-1]
            Reverse the DataFrame and find the last index where the condition is met
            '''
            start_index = price_df[::-1][price_df["Date"] > reported_date].index[0]
            end_index = start_index - time_window

            '''
            Check if end_index is within the DataFrame's index range
            '''
            if end_index < len(price_df):
                price_data_within_window = price_df.loc[end_index:start_index]
                print(price_data_within_window)
                '''
                Calculate the number of trading days within the time window
                '''
                trading_days_count = len(price_data_within_window)

                if trading_days_count >= time_window:
                    '''
                    Calculate the price drift
                    '''
                    final_price = price_data_within_window.iloc[0]["Close Price"]
                    
                    initial_price = price_data_within_window.iloc[time_window]["Close Price"]
                    
                    price_drift = final_price - initial_price
                    '''
                    Append data to the combined data list as a dictionary
                    '''
                    combined_data.append({
                        "reportedDate": reported_date,
                        "surprisePercentage": surprise_percentage,
                        "ticker": ticker,
                        "priceDrift": price_drift
                    })

    combined_df = pd.DataFrame(combined_data)

    '''
    Save the combined DataFrame to a CSV file
    '''
    combined_df.to_csv('data/earnings_drift.csv', index=False)
    clean_data(df=combined_df, filename='data/earnings_drift.csv')
    print(combined_df)






if __name__ == "__main__":
    # get_small_cap_close_data()
    # get_small_cap_earnings_data()
    calc_earnings_drift()