import pandas as pd
import utilities as util
import math, sys

def emaCrossover(path, window):
    print("--------------------")
    print("Running EMA" + str(window) + " Crossover Strategy.")
    print("--------------------")
    emaColumn = "ema" + str(window)
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    startingBalance = 1000000
    balance = startingBalance
    unitsAvailable = 0
    long = False


    for i in range(2, count):
        if (dataframe.iloc[i-2]["low"] < dataframe.iloc[i-2][emaColumn]) and (dataframe.iloc[i-2]["close"] > dataframe.iloc[i-2][emaColumn]) and (dataframe.iloc[i-1]["close"] > dataframe.iloc[i-1][emaColumn]) and (dataframe.iloc[i]["close"] > dataframe.iloc[i][emaColumn])and (dataframe.iloc[i]["low"] > dataframe.iloc[i][emaColumn]) and  (not long) :
            qty = math.floor(balance/dataframe.iloc[i]['close'])
            print (str(dataframe.iloc[i]["timestamp"]) + ": BUY " + str(qty) + " units at $" + str(dataframe.iloc[i]['close']))
            long = True
            balance -= dataframe.iloc[i]['close'] * qty
            unitsAvailable += qty
        elif(dataframe.iloc[i]["close"] < dataframe.iloc[i][emaColumn]) and (long) :
            print (str(dataframe.iloc[i]["timestamp"]) + ": SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
    if unitsAvailable > 0:
        balance += dataframe.iloc[count-1]["close"] * unitsAvailable
        print (str(dataframe.iloc[count-1]["timestamp"]) + ": FORCE SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[count-1]["close"]))


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
    #print (dataframe)
    sys.stdout.flush()
