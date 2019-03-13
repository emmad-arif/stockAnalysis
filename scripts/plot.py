import io, os

import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num, DayLocator, DateFormatter
import pandas as pd


def plot(path, *indicators):

    with open(path) as f:
        s = f.read() + '\n'

    my_file = pd.read_table(io.StringIO(s), sep=',', header=0)

    my_file['timestamp'] = date2num(pd.to_datetime(my_file['timestamp']).tolist())

    fig, ax=plt.subplots(figsize=(15,15))


    candlestick_ohlc(ax, my_file.as_matrix(), colorup='g', colordown='r', alpha=0.75)
    #ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    i = 0
    colors = ['#000000', "#FFFF00", "#0000FF", "#7CFC00"]
    for indicator in indicators:
        if not indicator in my_file.columns:
            print("Error in plot.py: " + indicator + " does not exist. Skipping.")
            pass
        ax.plot(my_file['timestamp'],my_file[indicator],colors[i],linewidth=2)
        i += 1
    plt.show()
