import pandas as pd

#return data
def appendSMA(dataframe, window):

    count = len(dataframe)
    if (window > count):
         print("ERROR: in sma.py specified window length > dataset length")
         return
    elif (window > count/2):
        print("WARNING: in sma.py - specified window length > dataset length/2")

    smaColumn = "sma" + str(window)
    dataframe["valid"] = "N"
    dataframe[smaColumn] = -1

    for i in range(0, count-window+1):
        #print("i: ", i)
        sum = 0
        for j in range(i, i+window):
            sum += dataframe.iloc[j]["close"]
        dataframe.iloc[i, dataframe.columns.get_loc(smaColumn)] = sum/window
        dataframe.iloc[i, dataframe.columns.get_loc('valid')] = "Y"
    #print(data)
    dataframe = dataframe[dataframe.valid == 'Y']
    dataframe = dataframe.drop(columns=['valid'])
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
