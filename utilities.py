from __future__ import print_function
import sys
from scripts.indicators import sma
import utilities as util


def printError(errorMessage):
    print("Error: " + errorMessage, file=sys.stderr)

def applyIndicator(dataframe, indicator):
    if "sma" in indicator:
        window = int(indicator[3:])
        #error check here
        dataframe = sma.appendSMA(dataframe, window)
        return dataframe
    else:
        util.printError("Invalid indicator: " + indicator)
        return False
