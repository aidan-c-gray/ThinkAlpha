'''
Analysis of bitcoin price and sentiment data
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
plot the price of bitcoin over time and save the image in the images folder
'''
def visualize_bitcoin_price():
    '''
    load bitcoin data from csv file
    '''
    bitcoin_price_df = pd.read_csv('data/bitcoin_daily_close.csv')


    '''
    ensure the date columns are in datetime format (if not already)
    '''
    bitcoin_price_df['Date'] = pd.to_datetime(bitcoin_price_df['Date'])

    '''
    plot figure for bitcoin over time and save to images folder
    '''
    plt.figure(figsize=(10, 6))
    plt.plot(bitcoin_price_df['Date'], bitcoin_price_df['Close Price'], linestyle='-')
    plt.title('Bitcoin Daily Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig('images/bitcoin_line_plot.png')

'''
visualize the bitcoin sentiment data by grouping it into bins based on score and plotting a histogram
'''
def visualize_sentiment():
    '''
    grab bitcoin sentiment data from csv file and print out quick summary
    '''
    df = pd.read_csv('data/bitcoin_sentiment.csv')
    print(df.head())
    print(df.describe())

    '''
    bins and the labels of the bins to sort the sentiment score into later
    '''
    bins = [-float('inf'), -0.35, -0.15, 0.15, 0.35, float('inf')]
    labels = ['bearish', 'somewhat_bearish', 'neutral', 'somewhat_bullish', 'bullish']
    
    df = df.dropna(subset=['Overall Sentiment Score'])

    '''
    create new column in df group and cut/separate them into the different bins and assign the appropriate label
    '''
    df['group'] = pd.cut(df['Overall Sentiment Score'], bins=bins, labels=labels, include_lowest=True)
    print(df)

    '''
    count the number of scores in each group
    '''
    group_counts = df['group'].value_counts().to_dict()

    '''
    Extract keys and values from the dictionary
    '''
    group = list(group_counts.keys())
    counts = list(group_counts.values())

    '''
    Create a bar plot and save image to images folder
    '''
    plt.figure(figsize=(8, 6))
    plt.bar(group, counts)
    plt.xlabel('Group')
    plt.ylabel('Count')
    plt.title('Counts of Groups')
    plt.savefig("images/bitcoin_sentiment")

# Hypothesis Testing (if applicable)
# Example: t-test, ANOVA, etc.

# Time Series Analysis (if applicable)
# Example: Decomposition, forecasting, etc.

# Machine Learning (if applicable)
# Example: Linear regression, classification, etc.

# Reporting and Visualization (create reports or dashboards)


if __name__ == "__main__":
    symbol = "BTCUSD"
    visualize_bitcoin_price()
    visualize_sentiment()
    # Retrieve Bitcoin price data

