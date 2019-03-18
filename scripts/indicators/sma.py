import pandas as pd
import math
import sys


#return data
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
    dataframe["valid"] = "N"
    dataframe[smaColumn] = -1
    """
    dataframe['MA'] = dataframe.close.rolling(window=window).mean()
    print(dataframe)
    exit()
    """
    if window == 1:
        dataframe[smaColumn] = dataframe['close']
        dataframe = dataframe.drop(columns=['valid']).reset_index(drop=True)
        print("SMA" + str(window) + " added to data")
        return dataframe

    for i in range(window-1, count):
        #print("i " + str(i) + "count " + str(count))
        sum = 0
        if (dataframe.ix[i-1][smaColumn] == -1):
            for j in range(i-window+1, i+1):
            #    print("j " + str(j))
                sum += dataframe.ix[j]["close"]
                #print(sum)
            dataframe.loc[i, smaColumn] = sum/window
            dataframe.loc[i, 'valid'] = "Y"
        #print ('\x1b[2K\r' + str(i))
        else:
            newSum = (dataframe.ix[i-1][smaColumn] * window) - dataframe.ix[i-window]['close'] + dataframe.ix[i]['close']
            dataframe.loc[i, smaColumn] = newSum/window
            dataframe.loc[i, 'valid'] = "Y"
    #print(data)

    dataframe = dataframe[dataframe.valid == 'Y']
    dataframe = dataframe.drop(columns=['valid']).reset_index(drop=True)
    print("\nSMA" + str(window) + " added to data.")
    #print(dataframe)
    sys.stdout.flush()
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
