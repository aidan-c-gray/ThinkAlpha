import os
import pandas as pd
import matplotlib.pyplot as plt


def visualize_csv():

    csv_files = ["AMR", "MO", "AMCX", "AMN", "ARCT", "ARHS", "BKE", "BBW", "CPRX", "LNG", "COLL", "CCSI", "CROX", "CVI", "EVRI", "FOXA", "GTX", "GCT", "GPOR", "HRB", "HRMY", "HSII", "HPQ", "IDCC", "IPG", "IRWD", "JILL", "JAKK", "LSXMK", "MBUU", "MCFT", "MED", "MLI", "NATH", "OMC", "PARR", "MD", "PRDO", "PLTK", "PINC", "RGP", "RMNI", "SMLR", "STGW", "TH", "UIS", "UNTC", "VGR", "VYGR", "ZYME"]

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

def visualize_tech():
    # Load and visualize the 'momentum_tech.csv' file
    tech = pd.read_csv('data/earnings_tech.csv')
    print(tech.head())

    # Show all plots
    plt.show()

def visualize_drift():
    # Load and visualize the 'momentum_tech.csv' file
    drift = pd.read_csv('data/earnings_drift.csv')
    print(drift.head())

    # Show all plots
    plt.show()

if __name__ == "__main__":
    visualize_csv()
    visualize_tech()
    visualize_drift()

