"""
Make sure to run this from base directory
"""

from scripts import pullData
from scripts.indicators import sma
import pandas as pd
import utilities as util
import sys, os



def pullAndEnrich(ticker, outputSize, rawDirectory, enrichDirectory, *indicators):
    ticker = ticker.upper()
    pulled = pull(ticker, rawDirectory, outputSize)
    if pulled:
        enrich(ticker, rawDirectory, enrichDirectory, *indicators)

def enrich(ticker, rawDirectory, enrichDirectory, *indicators):
    rawFile = rawDirectory + ticker.upper() + ".csv"
    outputFile = enrichDirectory + ticker.upper() + ".enriched.csv"

    if os.path.isfile(outputFile):
        replace = input(outputFile + " already exists. Replace? (Y/N)\n")
        if replace.upper() != "Y":
            return True

    try:
        data = pd.read_csv(rawFile)
    except:
        util.printError("Raw File not present. Enrich Failed.")
        return False

    for indicator in indicators:
        data = util.applyIndicator(data, indicator.lower())
    data.to_csv(outputFile, index=False)
    print(ticker + " Enrich Successful!")
    return True

def pull(ticker, rawDirectory, outputSize):
    # default pull is "full". Another option is "compact"
    outputFile = rawDirectory + ticker.upper() + ".csv"
    if os.path.isfile(outputFile):
        replace = input(outputFile + " already exists. Replace? (Y/N)\n")
        if replace.upper() != "Y":
            return True
    #outputSize = "full"
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&interval=5min&outputsize=" + outputSize + "&apikey=JN3OXB2JR2CV2RDO&datatype=csv"
    data = pd.read_csv(url)
    if errorCheck(data):
        return False

    data.to_csv(outputFile, index=False)
    util.cutCsv(outputFile)

    print(ticker + " Pull Successful!")
    return True


# Find something less hacky???
def errorCheck(dataframe):
    if "Error" in dataframe.to_string():
        util.printError("Pull Failed.")
        return True
    return False
