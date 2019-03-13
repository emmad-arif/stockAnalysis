import pandas as pd
import utilities as util
import math

def smaLongShortCrossover(path, longWindow, shortWindow):
    longSMAColumn = "sma" + str(longWindow)
    shortSMAColumn = "sma" + str(shortWindow)
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    startingBalance = 1000000
    balance = startingBalance
    unitsAvailable = 0
    long = False
    lastPrice = 0

    for i in range(count-1, -1, -1):
        if (dataframe.iloc[i][shortSMAColumn] > dataframe.iloc[i][longSMAColumn]) and (not long):
            qty = math.floor(balance/dataframe.iloc[i]["close"])
            print (str(dataframe.iloc[i]["timestamp"]) + ": BUY " + str(qty) + " units at $" + str(dataframe.iloc[i]["close"]))
            long = True
            balance -= dataframe.iloc[i]["close"] * qty
            unitsAvailable += qty
            lastPrice = dataframe.iloc[i]["close"]
        elif (dataframe.iloc[i][shortSMAColumn] < dataframe.iloc[i][longSMAColumn]) and (long): # and dataframe.iloc[i]["close"] > lastPrice:
            print (str(dataframe.iloc[i]["timestamp"]) + ": SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
    if unitsAvailable > 0:
        balance += dataframe.iloc[0]["close"] * unitsAvailable


    returnPercentage = 100*((balance-startingBalance)/startingBalance)
    period = util.periods(dataframe)/365

    avgReturnPercentage = round(returnPercentage/period, 2)
    period = round(period, 2)
    returnPercentage = round(returnPercentage, 2)
    balance = round(balance, 2)

    print("\nBalance: " + str(balance) + "\nReturn Percentage: " + str(returnPercentage) + "% over a period of " + str(period) + " years.")
    print("Average Yearly Return Percentage: " + str(avgReturnPercentage) + "%")
    #print (dataframe)



def smaCrossover(path, window):
    smaColumn = "sma" + str(window)
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    startingBalance = 1000000
    balance = startingBalance
    unitsAvailable = 0
    long = False


    for i in range(count-1, -1, -1):
        if (dataframe.iloc[i]["close"] > dataframe.iloc[i][smaColumn]) and (not long):
            qty = math.floor(balance/dataframe.iloc[i]["close"])
            print (str(dataframe.iloc[i]["timestamp"]) + ": BUY " + str(qty) + " units at $" + str(dataframe.iloc[i]["close"]))
            long = True
            balance -= dataframe.iloc[i]["close"] * qty
            unitsAvailable += qty
        elif (dataframe.iloc[i]["close"] < dataframe.iloc[i][smaColumn]) and (long):
            print (str(dataframe.iloc[i]["timestamp"]) + ": SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
    if unitsAvailable > 0:
        balance += dataframe.iloc[0]["close"] * unitsAvailable


    returnPercentage = 100*((balance-startingBalance)/startingBalance)
    period = util.periods(dataframe)/365

    avgReturnPercentage = round(returnPercentage/period, 2)
    period = round(period, 2)
    returnPercentage = round(returnPercentage, 2)
    balance = round(balance, 2)

    print("\nBalance: " + str(balance) + "\nReturn Percentage: " + str(returnPercentage) + "% over a period of " + str(period) + " years.")
    print("Average Yearly Return Percentage: " + str(avgReturnPercentage) + "%")
    #print (dataframe)
