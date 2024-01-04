import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data():
    # Load cleaned data
    sentiment_df = pd.read_csv('data/bitcoin_sentiment.csv')
    bitcoin_price_df = pd.read_csv('data/bitcoin_daily_close.csv')


    # Ensure the date columns are in datetime format (if not already)
    bitcoin_price_df['Date'] = pd.to_datetime(bitcoin_price_df['Date'])

    # Drop non-numeric columns before calculating correlations
    numeric_columns = bitcoin_price_df.select_dtypes(include='number')
    correlation_matrix = numeric_columns.corr()

    # Exploratory Data Analysis
    print(sentiment_df.head())
    print(bitcoin_price_df.head())

    # Data Visualization
    plt.figure(figsize=(10, 6))
    sns.histplot(data=bitcoin_price_df, x='Close Price', bins=20)
    plt.title('Bitcoin Daily Close Price Distribution')
    plt.xlabel('Close Price')
    plt.ylabel('Frequency')
    plt.show()

    # Statistical Analysis
    print(sentiment_df.describe())
    print(bitcoin_price_df.corr())

# Hypothesis Testing (if applicable)
# Example: t-test, ANOVA, etc.

# Time Series Analysis (if applicable)
# Example: Decomposition, forecasting, etc.

# Machine Learning (if applicable)
# Example: Linear regression, classification, etc.

# Reporting and Visualization (create reports or dashboards)


if __name__ == "__main__":
    symbol = "BTCUSD"
    visualize_data()
    # Retrieve Bitcoin price data

