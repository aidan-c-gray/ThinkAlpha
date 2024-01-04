import os
import pandas as pd
import matplotlib.pyplot as plt
from src.alpha_strategy_momentum import get_largest_tech_stocks


def visualize_csv():

    csv_files = get_largest_tech_stocks()
    # Load the CSV file into a DataFrame
    for ticker in csv_files:
        filename = f'data/{ticker}_daily_close.csv'
        df = pd.read_csv(filename)
        print(df.head())
        # Plot the data
        # plt.figure(figsize=(10, 6))
        # plt.plot(df['Date'], df['Close Price'], label=file_name[:-16])  # Extract ticker from file name
        # plt.title('Daily Close Price')
        # plt.xlabel('Date')
        # plt.ylabel('Close Price')
        # plt.legend()
        # plt.grid(True)

def visualize_momentum():
    # Load and visualize the 'momentum_tech.csv' file
    momentum_df = pd.read_csv('data/momentum_tech.csv')
    print(momentum_df.head())

    # Show all plots
    plt.show()

if __name__ == "__main__":
    visualize_csv()
    visualize_momentum()

