import io, os, sys

import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num, DayLocator, DateFormatter
import pandas as pd
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def plot(ticker, path, buys, sells, strategy):

    with open(path) as f:
        s = f.read() + '\n'

    my_file = pd.read_csv(io.StringIO(s), sep=',', header=0)

    my_file['timestamp'] = pd.to_datetime(my_file['timestamp']).tolist()

    t = my_file['timestamp']
    s = my_file['close']

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='Date', ylabel='Close Price ($)',
           title=ticker + " "+ strategy)
    ax.grid()

    for buy in buys:
        plt.axvline(x=buy, color="green", linewidth=0.3)

    for sell in sells:
        plt.axvline(x=sell, color="red", linewidth=0.3)


    print("\nPlotting " + ticker + " "+ strategy)
    print("Verticle green lines = BUY")
    print("Verticle red lines = SELL")
    print("Close plot to continue script.")
    sys.stdout.flush()
    plt.show()
#    plt.show()
