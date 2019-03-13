import pandas as pd

#return data
def appendSMA(dataframe, window):

    count = len(dataframe)
    if (window > count):
         print("ERROR: in sma.py specified window length > dataset length")
         return
    elif (window > count/2):
        print("WARNING: in sma.py - specified window length > dataset length/2")

    dataframe["valid"] = "N"
    dataframe["sma"] = -1

    for i in range(0, count-window+1):
        #print("i: ", i)
        sum = 0
        for j in range(i, i+window):
            sum += dataframe.iloc[j]["close"]
        dataframe.iloc[i, dataframe.columns.get_loc('sma')] = sum/window
        dataframe.iloc[i, dataframe.columns.get_loc('valid')] = "Y"
    #print(data)
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
