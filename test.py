import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime
import pandas as pd
pd.set_option("display.max_columns", None)

MACD_difference_tolerance_for_zero = 0.03
MACD_difference_tolerance_for_clarity = 0.05

def macd_buy_signal(ticker):

    # Deriving the values
    exp1 = ticker.ewm(span=12, adjust=False).mean()
    exp2 = ticker.ewm(span=26, adjust=False).mean()
    macd = (exp1 - exp2)['Close']
    signal_line = macd.ewm(span=9, adjust=False).mean()
    moving_avg = ticker['Close'].rolling(window=200).mean()

    # Exit condition if the stock can not be analyzed
    if len(signal_line) < 10:
        return False
    
    # The price being above moving average will indicate the trend is upwards, thus a higher chance of increase (Recommended Trading Rush)
    price_above_moving_average = moving_avg.iloc[-1] < ticker['Close'].iloc[-1]

    # Ensuring that a crossover happens (Recommended Trading Rush)
    MACD_in_tolerance = abs(macd.iloc[-1] - signal_line.iloc[-1]) < MACD_difference_tolerance_for_zero

    # The current MACD value should be less than 0 (Recommended Trading Rush)
    MACD_less_than_zero = macd.iloc[-1] < 0

    # Ensure the MACD and the signal line have not been close previously (Individual criteria I inserted)
    clear_MACD_buy_signal = signal_line.iloc[-2] - macd.iloc[-2] > MACD_difference_tolerance_for_clarity

    # The price from the previous day should not increase more than 4% (Individual criteria I inserted)
    not_an_upwards_spike = (ticker['Close'].iloc[-1]/ticker['Close'].iloc[-2]) <= 1.04

    # Combine all criteria and generate a boolean signal to buy or avoid
    send_buy_signal = MACD_in_tolerance and price_above_moving_average and MACD_less_than_zero and clear_MACD_buy_signal and not_an_upwards_spike
    return send_buy_signal

# Obtaining the nasdaq symbols and converting the filtered list to a numpy array
tickers = pdr.get_nasdaq_symbols()
tickers = tickers.loc[~tickers['Test Issue']]['NASDAQ Symbol'].to_numpy()

# Iterate through the nasdaq symbols
for i in tickers:
    try:
        ticker_info = pdr.get_data_yahoo(i , start=datetime.datetime(2020, 2, 1), end=datetime.datetime.now())
    except:
        continue
    if macd_buy_signal(ticker_info):
        print("Buy Signal: " + i)
