import requests

# Replace 'YOUR_API_KEY' with your actual AlphaVantage API key
api_key = '14D92VU61DT8FVKO'

# Define the symbols for WTI and natural gas
wti_symbol = 'WTI'  # WTI (West Texas Intermediate) crude oil
ng_symbol = 'NG'    # Natural gas futures

# Define the output mode (either 'json' or 'csv')
output_mode = 'csv'  # You can choose 'json' or 'csv'
interval = '15min'    # The interval for news data (e.g., '15min', '30min', '60min', 'daily')

# Make requests to get news data for WTI and natural gas
wti_news_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={wti_symbol}&interval={interval}&apikey={api_key}'
ng_news_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ng_symbol}&interval={interval}&apikey={api_key}'

# Function to fetch and print news data
def fetch_and_print_news(url, commodity_name):
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        
        # Extract and print the news headlines
        print(f"News for {commodity_name}:")
        for date, news_item in news_data['Time Series (15min)'].items():
            print(f"Date: {date}, Headline: {news_item['1. open']}")
    else:
        print(f"Error: Unable to retrieve news data for {commodity_name}. Status code: {response.status_code}")

# Fetch news data for WTI
fetch_and_print_news(wti_news_url, 'WTI Crude Oil')

# Fetch news data for natural gas
fetch_and_print_news(ng_news_url, 'Natural Gas')
