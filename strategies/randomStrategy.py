import pandas as pd
import utilities as util
import math, sys
import random

def runMultipleRandoms(path, count):
    returnPct = 0
    for i in range(0, count):
        #print("HHHHH")
        returnPct += random(path)
    return round(returnPct/count, 2)

def random(path):
    dataframe = pd.read_csv(path)
    count = len(dataframe)

    startingBalance = 1000000
    balance = startingBalance
    unitsAvailable = 0
    long = False

    for i in range(0, count):
        if (randomGenerator) and (not long) :
            qty = math.floor(balance/dataframe.iloc[i]["close"])
            #print (str(dataframe.iloc[i]["timestamp"]) + ": BUY " + str(qty) + " units at $" + str(dataframe.iloc[i]["close"]))
            long = True
            balance -= dataframe.iloc[i]["close"] * qty
            unitsAvailable += qty
        elif (long):
            #print (str(dataframe.iloc[i]["timestamp"]) + ": SELL " + str(unitsAvailable) + " at $" + str(dataframe.iloc[i]["close"]))
            long = False
            balance += dataframe.iloc[i]["close"] * unitsAvailable
            unitsAvailable = 0
    if unitsAvailable > 0:
        balance += dataframe.iloc[0]["close"] * unitsAvailable


    returnPercentage = 100*((balance-startingBalance)/startingBalance)
    period = util.periods(dataframe)/365

    avgReturnPercentage = round(returnPercentage/period, 2)
    period = round(period, 2)

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
