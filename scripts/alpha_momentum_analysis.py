'''
Analysis of the daily close data for large tech stocks and the 
analysis of the daily momentum for large tech stocks
'''
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.alpha_strategy_momentum import get_largest_tech_stocks

'''
plot the price of the largest tech stocks over time and save the image in the images folder
'''
def visualize_tech_stock_price():

    '''
    grab list of tech stocks and for each one pull the associated csv and visualize the head of data and plot the graph
    '''
    csv_files = get_largest_tech_stocks()
    for ticker in csv_files:
        filename = f'data/{ticker}_daily_close.csv'
        df = pd.read_csv(filename)
        print(df.head())

        '''
        ensure the date columns are in datetime format (if not already)
        '''
        df['Date'] = pd.to_datetime(df['Date'])

        '''
        Drop non-numeric columns before calculating correlations
        '''
        numeric_columns = df.select_dtypes(include='number')

        '''
        plot figure for current tech stock and save to images folder
        '''
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Close Price'], linestyle='-')
        plt.title(f'{ticker} Daily Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'images/{ticker}_line_plot.png')


'''
visualizes the momentum data for the largest 20 tech stocks.
visualized using line plot of each individual company and a heatmap of all companies
'''
def visualize_momentum():
    '''
    load data from csv and visualize head of data
    '''
    df = pd.read_csv('data/momentum_tech.csv')
    print(df.head())

    '''
    for each company in the ticker column of the df plot the momentum score over time 
    '''
    unique_tickers = df['ticker'].unique()
    for ticker in unique_tickers:
        ticker_data = df[df['ticker'] == ticker]
        plt.plot(ticker_data['date'], ticker_data['mom_score'], label=ticker)
        plt.title(f'{ticker} Daily Momentum')
        plt.xlabel('Date')
        plt.ylabel('Momentum')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'images/{ticker}_mom_line_plot.png')

    '''
    Pivot the data for a heatmap and plot the heap map containing every tech stock in the dataframe
    '''
    pivot_df = df.pivot(index='date', columns='ticker', values='mom_score')
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_df, cmap='coolwarm')
    plt.xlabel('Ticker')
    plt.ylabel('Date')
    plt.title('Momentum Heatmap Over Time')
    plt.savefig(f'images/mom_heat_plot.png')


'''
Next Step:

When momentum is positive and above either 1 std or 2 std of the mean see how the stocks perform over the next x days (range)
Do the same for negative and 1 or 2 std below the mean. Find out optimal range to hold

Hypothese: positive momentum should continue for x number of days and negative momentum should continue for y number of days
and shorting negative momentum stocks and long positive momentum stocks 
'''

if __name__ == "__main__":
    # visualize_tech_stock_price()
    visualize_momentum()

