import pandas as pd
from scripts.indicators import sma
import sys
#return data
def appendEMA(dataframe, window):
    #check to see sma is present else add temporarily
    addedEMA = False
    if not ("sma" + str(window)) in dataframe.columns:
        dataframe = sma.appendSMA(dataframe, window)
        addedEMA = True
    count = len(dataframe)
    if (window > count):
         print("\nERROR: In EMA " + window + " calculation - specified horizon > dataset length")
         sys.stdout.flush()
         return dataframe
    elif (window > count/2):
        print("\nWARNING: In Ema " + window + " calculation - specified horizon > dataset length/2")
        sys.stdout.flush()

    alpha = 2/(window+1)

    emaColumn = "ema" + str(window)
    smaColumn = "sma" + str(window)
    dataframe[emaColumn] = -1
    dataframe.iloc[0, dataframe.columns.get_loc(emaColumn)] = dataframe.iloc[0][smaColumn]

    for i in range(1, count):
        ema = (dataframe.iloc[i]["close"] - dataframe.iloc[i-1][emaColumn]) * alpha + dataframe.iloc[i-1][emaColumn]
        dataframe.iloc[i, dataframe.columns.get_loc(emaColumn)] = ema
    if addedEMA:
        dataframe = dataframe.drop(columns=["sma"+str(window)]).reset_index(drop=True)
    #print(data)
    print("\nEMA" + str(window) + " added to data.")
    sys.stdout.flush()
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
