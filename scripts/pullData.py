"""
This script pulls daily closing data for a ticker symbol, and saves it to data/out.csv
Usage: pullData.py [TICKER SYMBOL] [ALL]*

Use ALL if you want entire dataset. Default is last 100 points.
"""

import pandas as pd
import sys



def pull(symbol, full=False):
    """
    if len(sys.argv) < 2:
        print("usage: pullData.py [TICKER SYMBOL] [ALL]*")
        exit()

    if len(sys.argv) == 3:
        if lower(sys.argv[2]) == "all":
            outputSize = "full"

    ticker = sys.argv[1]
    """
    ticker = symbol
    outputSize = "compact"
    if full:
        outputSize = "full"
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&interval=5min&outputsize=" + outputSize + "&apikey=JN3OXB2JR2CV2RDO&datatype=csv"

    #error check
    data = pd.read_csv(url)
    #print(data)
    outputFile = "data/raw/" + ticker.upper() + ".csv"
    #print(outputFile)
    data.to_csv(outputFile, index=False)
