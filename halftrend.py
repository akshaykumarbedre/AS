import numpy as np
import  ta
import yfinance as yf
import pandas as pd
interval = "15m"     #interval : str: ->1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo 
period="1mo"    #period : str:-> 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
start=None          #start: str:->Download start date string (YYYY-MM-DD) Default is 1900-01-01
end=None     
company= "HDFCBANK.NS"
import matplotlib.pyplot as plt

df=yf.download(tickers=company,interval=interval,start=start,period=period,end=end)


low=df['Low']
high=df['High']
close=df['Close']

# Input variables
amplitude = 2
channelDeviation = 2
showArrows = False
showChannels = False

# Initialize variables
trend = 0
nextTrend = 0
maxLowPrice = np.nan
minHighPrice = np.nan
up = 0.0
down = 0.0
atrHigh = 0.0
atrLow = 0.0
arrowUp = np.nan
arrowDown = np.nan

# Calculate ATR
atr = ta.volatility.AverageTrueRange(high, low, close, window=100).average_true_range()
atr2 = atr / 2

# Calculate HalfTrend
highPrice = high.abs().rolling(window=amplitude).max()
lowPrice = low.abs().rolling(window=amplitude).min()
highma = high.rolling(window=amplitude).mean()
lowma = low.rolling(window=amplitude).mean()

# Calculate HalfTrend signals
for i in range(len(df)):
    if nextTrend == 1:
        maxLowPrice = max(lowPrice[i], maxLowPrice)
        if highma[i] < maxLowPrice and close[i] < df['Low'].shift(1)[i]:
            trend = 1
            nextTrend = 0
            minHighPrice = highPrice[i]
    else:
        minHighPrice = min(highPrice[i], minHighPrice)
        if lowma[i] > minHighPrice and close[i] > df['High'].shift(1)[i]:
            trend = 0            
            nextTrend = 1
            maxLowPrice = lowPrice[i]

    if trend == 0:
        if not np.isnan(trend.shift(1)[i]) and trend.shift(1)[i] != 0:
            up = down.shift(1)[i] if np.isnan(down.shift(1)[i]) else down.shift(1)[i]
            arrowUp = up - atr2[i]
        else:
            up = maxLowPrice if np.isnan(up.shift(1)[i]) else max(maxLowPrice, up.shift(1)[i])
        atrHigh[i] = up + channelDeviation * atr2[i]
        atrLow[i] = up - channelDeviation * atr2[i]
    else:
        if not np.isnan(trend.shift(1)[i]) and trend.shift(1)[i] != 1:
            down = up.shift(1)[i] if np.isnan(up.shift(1)[i]) else up.shift(1)[i]
            arrowDown = down + atr2[i]
        else:
            down = minHighPrice if np.isnan(down.shift(1)[i]) else min(minHighPrice, down.shift(1)[i])
        atrHigh[i] = down + channelDeviation * atr2[i]
        atrLow[i] = down - channelDeviation * atr2[i]

    ht = up if trend == 0 else down
    df.loc[i, 'HalfTrend'] = ht
    # df.loc[i, 'ATR High'] = atrHigh[i] if showChannels else np.nan
    # df.loc[i, 'ATR Low'] = atrLow[i] if showChannels else np.nan
    # if showArrows:
    #     buySignal = not np.isnan(arrowUp[i]) and trend[i] == 0 and trend.shift(1)[i] == 1
    #     sellSignal = not np.isnan(arrowDown[i]) and trend[i] == 1 and trend.shift(1)[i] == 0
