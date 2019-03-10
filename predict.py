import pandas as pd
from scripts import pullData, plot, sma
import sys

if len(sys.argv) < 2:
    print("usage: predict.py TICKER -pull -full -sma")
    exit()

#make list of tickers
ticker = sys.argv[1]
if "-pull" in sys.argv:
    if "-full" in sys.argv:
        pullData.pull(ticker, True)
    else:
        pullData.pull(ticker)
sma.appendSMA(ticker, 5)
if "-sma" in sys.argv:
    plot.plot(ticker, "sma")
else:
    plot.plot(ticker)
