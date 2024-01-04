'''
Analysis of small cap value stocks through visualization of price data 
'''
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.alpha_strategy_PEAD import get_small_cap_value

'''
plot the price of a list of small cap value stocks over time and save the image in the images folder
'''
def visualize_tech_stock_price():

    '''
    grab list of small cap value stocks and for each one pull the associated csv and visualize the head of data and plot the graph
    '''
    csv_files = get_small_cap_value()
    for ticker in csv_files:
        filename = f'data/{ticker}_daily_close.csv'
        df = pd.read_csv(filename)
        print(df.head())

        '''
        ensure the date columns are in datetime format (if not already)
        '''
        df['Date'] = pd.to_datetime(df['Date'])

        '''
        plot figure for current stock and save to images folder
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
Next steps:

Visualize earnings drift data and find the optimal earnings suprise percentage to go long or short for
50 days after the earnings are reported. 
'''


if __name__ == "__main__":
    visualize_tech_stock_price()

