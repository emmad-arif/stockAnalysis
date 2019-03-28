from __future__ import print_function
import sys, os
from scripts.indicators import sma, ema, rsi
import utilities as util
import pandas as pd
import datetime

def printError(errorMessage):
    print("Error: " + errorMessage, file=sys.stderr)

def applyIndicator(dataframe, indicator):
    if "sma" in indicator:
        #print(indicator)
        window = int(indicator[3:])
        #error check here
        dataframe = sma.appendSMA(dataframe, window)

        return dataframe
    elif "ema" in indicator:
        window = int(indicator[3:])
        #error check here
        dataframe = ema.appendEMA(dataframe, window)
        return dataframe
    elif "rsi" in indicator:
        window = (indicator[3:])
        if window == "":
            dataframe = rsi.appendRSI(dataframe)
        else:
            dataframe = rsi.appendRSI(dataframe, int(window))
        return dataframe
    else:
        util.printError("Invalid indicator: " + indicator)
        return dataframe

# Deletes all entries before a certain date
def cutCsv(dataframe, date = datetime.datetime.strptime("2015-01-01", '%Y-%m-%d').date()):
    count = len(dataframe)

    cut = -1
    for i in range(0, count):
        if (datetime.datetime.strptime(dataframe.iloc[i]["timestamp"], '%Y-%m-%d').date()) < date:
            cut = i
            break
    if cut != -1:
        dataframe = dataframe[0:cut]
    #print(datetime.datetime.strptime(dataframe.iloc[0]["timestamp"], '%Y-%m-%d').date())
    if (datetime.datetime.strptime(dataframe.iloc[0]["timestamp"], '%Y-%m-%d').date()) == datetime.datetime.today().date():
        dataframe = dataframe[1:len(dataframe)]
        #print("Cut Successful!")
    return dataframe

# Returns number of periods from start to end
def periods(path):
    dataframe = pd.read_csv(path)
    count = len(dataframe)
    lastDate = datetime.datetime.strptime(dataframe.iloc[count-1]["timestamp"], '%Y-%m-%d').date()
    firstDate = datetime.datetime.strptime(dataframe.iloc[0]["timestamp"], '%Y-%m-%d').date()

    return (lastDate - firstDate).days

# Removes duplicates from list
def removeDuplicates(lst):
    lst = list(dict.fromkeys(lst))
    return lst

def printPartition():
    print("*******************************************************************************")
    sys.stdout.flush()
