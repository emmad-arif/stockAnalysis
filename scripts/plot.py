import io, os

import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num, DayLocator, DateFormatter
import pandas as pd


def plot(ticker, *indicators):
    path = ""
    for file in os.listdir("data/enriched"):
        if ticker.upper() in file:
            path = "data/enriched/" + file
    if path == "":
        print("ERROR: plot.y - file not found")
        return

    with open(path) as f:
        s = f.read() + '\n'

    my_file = pd.read_table(io.StringIO(s), sep=',', header=0)

    my_file['timestamp'] = date2num(pd.to_datetime(my_file['timestamp']).tolist())

    fig, ax=plt.subplots(figsize=(15,15))


    candlestick_ohlc(ax, my_file.as_matrix(), colorup='g', colordown='r', alpha=0.75)
    #ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    if "sma" in indicators:
        plotSMA(ax, my_file);
    plt.show()

def plotSMA(ax, my_file):
    ax.plot(my_file['timestamp'],my_file['sma'],'#000000',linewidth=2)
