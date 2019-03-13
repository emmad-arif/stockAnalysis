from __future__ import print_function
import sys, os
from scripts.indicators import sma, ema
import utilities as util
import pandas as pd
import datetime

def printError(errorMessage):
    print("Error: " + errorMessage, file=sys.stderr)

def applyIndicator(dataframe, indicator):
    if "sma" in indicator:
        window = int(indicator[3:])
        #error check here
        dataframe = sma.appendSMA(dataframe, window)
        return dataframe
    elif "ema" in indicator:
        window = int(indicator[3:])
        #error check here
        dataframe = ema.appendEMA(dataframe, window)
        return dataframe
    else:
        util.printError("Invalid indicator: " + indicator)
        return False

# Deletes all entries before a certain date
def cutCsv(path, date):
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    cut = -1
    for i in range(0, count):
        if (datetime.datetime.strptime(dataframe.iloc[i]["timestamp"], '%Y-%m-%d').date()) < date:
            cut = i
            break
        if cut != -1:
            dataframe = dataframe[0:cut]
            dataframe.to_csv(path, index=False)

# Returns number of periods from start to end
def periods(dataframe):
    count = len(dataframe)
    lastDate = datetime.datetime.strptime(dataframe.iloc[0]["timestamp"], '%Y-%m-%d').date()
    firstDate = datetime.datetime.strptime(dataframe.iloc[count-1]["timestamp"], '%Y-%m-%d').date()

    return (lastDate - firstDate).days
