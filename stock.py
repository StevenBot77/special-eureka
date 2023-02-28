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

# Calculate Bollinger Bands
def compute_bollinger_bands(df, window=20, num_std=2):
  sma = df['Close'].rolling(window=window).mean()
  std = df['Close'].rolling(window=window).std()
  upper_band = sma + num_std * std
  lower_band = sma - num_std * std
  return upper_band, lower_band

sp500_data['BBupper'], sp500_data['BBlower'] = compute_bollinger_bands(sp500_data)

# Calculate RSI
def compute_RSI(df, n=14):
  deltas = np.diff(df['Close'])
  seed = deltas[:n+1]
  up = seed[seed>=0].sum()/n
  down = -seed[seed<0].sum()/n
  rs = up/down
  rsi = np.zeros_like(df['Close'])
  rsi[:n] = 100. - 100./(1.+rs)
  for i in range(n, len(df['Close'])):
    delta = deltas[i-1] # cause the diff is 1 shorter
    if delta>0:
      upval = delta
      downval = 0.
    else:
      upval = 0.
      downval = -delta
    up = (up*(n-1) + upval)/n
    down = (down*(n-1) + downval)/n
    rs = up/down
    rsi[i] = 100. - 100./(1.+rs)
  return rsi

sp500_data['RSI'] = compute_RSI(sp500_data)

# Convert date strings to dates
sp500_data['Date'] = pd.to_datetime(sp500_data.index)
sp500_data['Date'] = sp500_data['Date'].apply(mdates.date2num)

# Create candlestick & RSI chart
ohlc = sp500_data[['Date', 'Open', 'High', 'Low', 'Close']]
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red')

ax1.plot(sp500_data['Date'], sp500_data['BBupper'], 'b--', linewidth=1.5, label='Upper Bollinger Band')
ax1.plot(sp500_data['Date'], sp500_data['SMA20'], 'y--', linewidth=1.5, label='20-day Simple Moving Average')
ax1.plot(sp500_data['Date'], sp500_data['SMA50'], 'm--', linewidth=1.5, label='50-day Simple Moving Average')
ax1.plot(sp500_data['Date'], sp500_data['BBlower'], 'g--', linewidth=1.5, label='Lower Bollinger Band')

ax2.plot(sp500_data['Date'], sp500_data['RSI'], 'b-', linewidth=1.5)

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


event_idxs = sp500_data.index.isin(event_dates)

event_lows = sp500_data.loc[event_idxs, 'Low'].values
event_dates = sp500_data.loc[event_idxs, 'Date'].values

for event in events:
  event_date = mdates.date2num(pd.to_datetime(str(event['date'])))
  ax1.annotate(event['label'], xy=(event_date, sp500_data.loc[event['date']]['Low']), xytext=(event_date, -300),
                rotation=90, va='bottom', ha='center', fontsize=10,
                arrowprops=dict(facecolor='black', shrink=0.05))
  ax1.annotate(event['text'], xy=(event_date, sp500_data.loc[event['date']]['Low']), xytext=(event_date+5, sp500_data.loc[event['date']]['Low']+30),
                fontsize=8, ha='left', va='center',
                arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle='arc3'))


# Style Chart
ax1.set_title('S&P500 Candlestick & Moving Averages & Bollinger Bands & RSI Chart', fontsize=14)
ax1.set_xlabel('Date', fontsize=10)
ax1.set_ylabel('Price in USD', fontsize=10)
ax1.tick_params(axis='x', rotation=45)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
ax1.xaxis.set_minor_locator(mdates.DayLocator())
plt.setp(ax1.get_xticklabels(), visible=True)

ax2.set_xlabel('Date', fontsize=10)
ax2.set_ylabel('Relative Strength Index', fontsize=10)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
ax2.xaxis.set_minor_locator(mdates.DayLocator())
plt.setp(ax2.get_xticklabels(), visible=True)
ax2.grid()

# Show plot
plt.show()