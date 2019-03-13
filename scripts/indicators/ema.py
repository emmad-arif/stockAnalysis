import pandas as pd

#return data
def appendEMA(dataframe, window):
    #check to see sma is present else add temporarily
    count = len(dataframe)
    if (window > count):
         print("ERROR: in ema.py specified window length > dataset length")
         return
    elif (window > count/2):
        print("WARNING: in ema.py - specified window length > dataset length/2")

    alpha = 2/(window+1)

    emaColumn = "ema" + str(window)
    smaColumn = "sma" + str(window)
    dataframe[emaColumn] = -1
    dataframe.iloc[count-1, dataframe.columns.get_loc(emaColumn)] = dataframe.iloc[count-1][smaColumn]

    for i in range(count-2, -1, -1):
        ema = (dataframe.iloc[i]["close"] - dataframe.iloc[i+1][emaColumn]) * alpha + dataframe.iloc[i+1][emaColumn]
        dataframe.iloc[i, dataframe.columns.get_loc(emaColumn)] = ema
    #print(data)
    return dataframe

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
