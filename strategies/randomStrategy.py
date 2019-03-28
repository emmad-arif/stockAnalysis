import pandas as pd
import utilities as util
import math, sys
import random
import tradeUtilities as tradeUtil
import config

def runMultipleRandoms(path, count):
    returnPct = 0
    for i in range(0, count):
        #print("HHHHH")
        returnPct += randomStrat(path)
    return round(returnPct/count, 2)

def randomStrat(path):
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    startingBalance = 1000000
    balance = startingBalance
    unitsAvailable = 0
    long = False
    lastBuy = -1
    for i in range(0, count):
        bool = randomGenerator()
        if (bool) and (not long) :
            qty = math.floor(balance/dataframe.iloc[i]["close"])
            #print (str(dataframe.iloc[i]["timestamp"]) + ": BUY " + str(qty) + " units at $" + str(dataframe.iloc[i]["close"]))
            long = True
            balance -= dataframe.iloc[i]["close"] * qty
            unitsAvailable += qty
            lastBuy = i
        elif (long) and not bool:
            #print (str(dataframe.iloc[i]["timestamp"]) + ": SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
            #print("Balance: " + str(balance))
    if unitsAvailable > 0:
        balance += dataframe.iloc[lastBuy]["close"] * unitsAvailable

    #print("Balance: " + str(balance))
    returnPercentage = 100*((balance-startingBalance)/startingBalance)
    #period = util.periods(dataframe)/365

    #avgReturnPercentage = round(returnPercentage/period, 2)
    #period = round(period, 2)

    balance = round(balance, 2)
    """
    print("\nBalance: " + str(balance) + "\nReturn Percentage: " + str(returnPercentage) + "% over a period of " + str(period) + " years.")
    print("Average Yearly Return Percentage: " + str(avgReturnPercentage) + "%")

    print("--------------------")
    """
    sys.stdout.flush()
    return returnPercentage
def randomGenerator():
    return random.choice([True, False])
