"""
Make sure to run this from base directory
"""

from scripts import pullData
from scripts.indicators import sma
import pandas as pd
import utilities as util
import sys, os



def pullAndEnrich(ticker, outputSize, rawDirectory, enrichDirectory, indicators):
    ticker = ticker.upper()
    pulled = pull(ticker, rawDirectory, outputSize)
    if pulled:
        enrich(ticker, rawDirectory, enrichDirectory, indicators)

def enrich(ticker, rawDirectory, enrichDirectory, indicators):
    rawFile = rawDirectory # + ticker.upper() + ".csv"
    outputFile = enrichDirectory # + ticker.upper() + ".enriched.csv"

    if os.path.isfile(outputFile):
        replace = input(outputFile + " already exists. Replace? (Y/N)\n")
        if replace.upper() != "Y":
            return True

    try:
        data = pd.read_csv(rawFile)
    except:
        print("\n" + ticker + " raw file not present. Cannot enrich.")
        sys.stdout.flush()
        return False

    for indicator in indicators:
        data = util.applyIndicator(data, indicator.lower())
    data.to_csv(outputFile, index=False)
    print("\n" + ticker + " enriched successfully.")
    return True

def pull(ticker, rawDirectory, outputSize):
    # default pull is "full". Another option is "compact"
    outputFile = rawDirectory # + ticker.upper() + ".csv"
    if os.path.isfile(outputFile):
        #print(outputFile + " already exists. To pull updated data, use -forcePull\n")
        #sys.stdout.flush()
        return True
    #    if replace.upper() != "Y":
    #        return True
    #outputSize = "full"
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&interval=5min&outputsize=" + outputSize + "&apikey=JN3OXB2JR2CV2RDO&datatype=csv"
    data = pd.read_csv(url)
    if errorCheck(data, ticker):
        return False
    data = util.cutCsv(data)
    data.iloc[:] = data.iloc[::-1].values

    data.to_csv(outputFile, index=False)


    print("\n" + ticker + " pulled successfully.")
    return True


# Find something less hacky???
def errorCheck(dataframe, ticker):
    if "Error" in dataframe.to_string():
        util.printError("\nERROR: " + ticker + " pull failed.")
        return True
    return False
