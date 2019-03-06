import pandas as pd

def appendSMA(symbol, windowLength):
    dataset="data/raw/" + symbol.upper() + ".csv"
    data = pd.read_csv(dataset)
    # error check if read fails
    #print(data.iloc[1][1])
    count = len(data)
    if (windowLength > count):
        print("ERROR: in sma.py - specified window length > dataset length")
        return 0
    elif (windowLength > count/2):
        print("WARNING: in sma.py - specified window length > dataset length/2")

    data["valid"] = "N"
    data["sma"] = -1

    for i in range(windowLength-1, count):
        #print("i: ", i)
        sum = 0
        for j in range(i-windowLength+1, i+1):
            sum += data.iloc[j]["close"]
        data.iloc[i, data.columns.get_loc('sma')] = sum/windowLength
        data.iloc[i, data.columns.get_loc('valid')] = "Y"
    #print(data)

    output = dataset[-9:-4]
    output = "data/enriched/" + output + ".SMA" + str(windowLength) + ".csv"
    data.to_csv(output, index=False)

    #else:
        # fix this
    #    return
        #data.to_csv(output, index=False)
#appendSMA(5)
