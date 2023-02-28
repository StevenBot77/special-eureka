import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np

# Load data
start_date = '2015-01-01'
end_date = '2022-12-31'
sp500_data = yf.download('^GSPC', start_date, end_date)

# Calculate moving averages
sp500_data['SMA20'] = sp500_data['Close'].rolling(window=20).mean()
sp500_data['SMA50'] = sp500_data['Close'].rolling(window=50).mean()

# Convert date strings to dates
sp500_data['Date'] = pd.to_datetime(sp500_data.index)
sp500_data['Date'] = sp500_data['Date'].apply(mdates.date2num)

# Create candlestick chart
ohlc = sp500_data[['Date', 'Open', 'High', 'Low', 'Close']]
fig, ax = plt.subplots(figsize=(10, 6))
candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red')

# Add economic events with annotations
events = [    
    {'date': '2015-12-16', 'label': 'Fed Raises Interest Rates', 'text': 'The Federal Reserve raised the federal funds rate by 0.25% for the first time in nearly a decade.'},    
    {'date': '2016-11-08', 'label': 'US Presidential Election', 'text': 'Donald Trump was elected as the 45th President of the United States.'},    
    {'date': '2017-12-13', 'label': 'Fed Raises Interest Rates', 'text': 'The Federal Reserve raised the federal funds rate by 0.25%, marking the fifth rate hike since the financial crisis.'},    
    {'date': '2018-11-06', 'label': 'US Midterm Elections', 'text': 'The United States held its midterm elections, resulting in a split Congress.'},    
    {'date': '2019-07-31', 'label': 'Fed Cuts Interest Rates', 'text': 'The Federal Reserve lowered the federal funds rate by 0.25%, citing concerns about global growth and trade tensions.'},    
    {'date': '2020-11-03', 'label': 'US Presidential Election', 'text': 'Joe Biden was elected as the 46th President of the United States.'},    
    {'date': '2021-06-16', 'label': 'Fed Expects Interest Rate Hikes', 'text': 'The Federal Reserve signaled that it expects to raise interest rates twice in 2023 and projected faster economic growth and inflation.'},
]
event_dates = pd.to_datetime([event['date'] for event in events])
event_idxs = sp500_data.index.isin(event_dates)

event_lows = sp500_data.loc[event_idxs, 'Low'].values
event_dates = sp500_data.loc[event_idxs, 'Date'].values

for event in events:
    event_date = mdates.date2num(pd.to_datetime(str(event['date'])))
    ax.annotate(event['label'], xy=(event_date, sp500_data.loc[event['date']]['Low']), xytext=(event_date, -500),
                rotation=90, va='bottom', ha='center', fontsize=10,
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate(event['text'], xy=(event_date, sp500_data.loc[event['date']]['Low']), xytext=(event_date+5, sp500_data.loc[event['date']]['Low']),
                fontsize=8, ha='left', va='center',
                arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle='arc3'))

# Set axis labels and title
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Price ($)', fontsize=12)
ax.set_title('S&P 500 Index with Economic Events', fontsize=14)

# Set axis tick label size
plt.xticks(fontsize=8, rotation=45)

# Set the x-axis tick intervals and labels
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.tick_params(axis='x', which='major', labelsize=8, rotation=45)

# Set the minor tick intervals
ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

# Set the x-axis tick labels using FixedLocator and FixedFormatter
xticks = ax.get_xticks()
xticklabels = [mdates.num2date(item).strftime('%Y-%m-%d') for item in xticks]
ax.xaxis.set_major_locator(plt.FixedLocator(xticks))
ax.set_xticklabels(xticklabels, rotation=45, ha='right')

# Show plot
plt.show()



