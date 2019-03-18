import pandas as pd
import utilities as util
import math, sys

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
    stoploss = -1
    entry = -1
    stoplossPCT = .25
    for i in range(1, count):

        if long and dataframe.iloc[i]['close'] <= stoploss:
            qty = math.floor(unitsAvailable * stoplossPCT)
            print (str(dataframe.iloc[i]["timestamp"]) + ": **PARTIAL STOP LOSS SELL** " + str(qty) + " at $" + str(dataframe.iloc[i]['close']))
            sys.stdout.flush()
            balance += dataframe.iloc[i]['close'] * qty
            unitsAvailable -= qty
            if unitsAvailable == 0:
                long = False
            stoploss = stoploss - 0.05*stoploss
            continue
        """
        if long and dataframe.iloc[i]['close'] >= 1.1*entry:
            print (str(dataframe.iloc[i]["timestamp"]) + ": **PROFIT SELL** " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]['close']))
            sys.stdout.flush()
            long = False
            balance += dataframe.iloc[i]['close'] * unitsAvailable
            unitsAvailable = 0
            continue
        """
        if (dataframe.iloc[i][shortSMAColumn] > dataframe.iloc[i][longSMAColumn]) and (not long)  and (dataframe.iloc[i-1][shortSMAColumn] < dataframe.iloc[i-1][longSMAColumn]):
            qty = math.floor(balance/dataframe.iloc[i]["close"])
            print (str(dataframe.iloc[i]["timestamp"]) + ": **BUY** " + str(qty) + " units at $" + str(dataframe.iloc[i]["close"]))
            sys.stdout.flush()
            long = True
            stoploss = dataframe.iloc[i]["close"]-0.05*dataframe.iloc[i]["close"]
            entry = dataframe.iloc[i]["close"]
            #print("Setting STOP LOSS at " + str(stoploss))
            sys.stdout.flush()
            balance -= dataframe.iloc[i]["close"] * qty
            unitsAvailable += qty
            lastPrice = dataframe.iloc[i]["close"]
        elif (dataframe.iloc[i][shortSMAColumn] < dataframe.iloc[i][longSMAColumn]) and (long) and (dataframe.iloc[i-1][shortSMAColumn] > dataframe.iloc[i-1][longSMAColumn]): # and dataframe.iloc[i]["close"] > lastPrice:
            print (str(dataframe.iloc[i]["timestamp"]) + ": **SELL** " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            sys.stdout.flush()
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
    if unitsAvailable > 0:
        balance += dataframe.iloc[i]["close"] * unitsAvailable
        print (str(dataframe.iloc[i]["timestamp"]) + ": **FORCE SELL** " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))


    returnPercentage = 100*((balance-startingBalance)/startingBalance)
    period = util.periods(dataframe)/365

    avgReturnPercentage = round(returnPercentage/period, 2)
    period = round(period, 2)
    returnPercentage = round(returnPercentage, 2)
    balance = round(balance, 2)

    print("\nBalance: " + str(balance) + "\nReturn Percentage: " + str(returnPercentage) + "% over a period of " + str(period) + " years.")
    #print("Average Yearly Return Percentage: " + str(avgReturnPercentage) + "%")

    print("Buy and Hold Return Percentage would have been: " + str(round(100*(dataframe.iloc[count-1]['close']-dataframe.iloc[0]['close'])/dataframe.iloc[0]['close'], 2)) + "%")
    print("I.e. Bought at $" + str(dataframe.iloc[0]['close']) + " on " + str(dataframe.iloc[0]['timestamp'] + " and sold at $" + str(dataframe.iloc[count-1]['close']) + " on " + str(dataframe.iloc[count-1]['timestamp'])))
    print("--------------------\n\n")
    sys.stdout.flush()

    #print (dataframe)
