import pandas as pd
import math
import sys

def appendSMA(dataframe, window):
    #print(dataframe)
    sys.stdout.flush()
    #percentages = [0, 20, 40, 60, 80, 100]
    count = len(dataframe)
    if (window > count):
         print("\nERROR: In SMA " + window + " calculation - specified horizon > dataset length")
         sys.stdout.flush()
         return dataframe
    elif (window > count/2):
        print("\nWARNING: In SMA " + window + " calculation - specified horizon > dataset length/2")
        sys.stdout.flush()

    smaColumn = "sma" + str(window)
    #dataframe["valid"] = "N"
    #dataframe[smaColumn] = -1

    dataframe[smaColumn] = dataframe.close.rolling(window=window).mean()
    #print(dataframe)

    dataframe = dataframe.iloc[window-1:]
    dataframe = dataframe.reset_index(drop=True)
    print("SMA" + str(window) + " added to data.")
    #print(dataframe)
    sys.stdout.flush()
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
