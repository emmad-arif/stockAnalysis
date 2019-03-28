import math
import config
# Returns new balance and units available

PERCENT_CHANGE = config.PERCENT_CHANGE
UNORDINARY_SELL_PERCENT = 1.00 # Sell this % when executing stopLoss or takeProfit orders

def ordinaryBuyMax(date, balance, price, unitsAvailable, display):
    qty = math.floor(balance/price)
    #print(type(date))
    if display:
        print(str(date) + ": BUY " + str(qty) + " units at $" + str(price))
    balance = balance - qty*price
    unitsAvailable += qty
    stopLoss = (1-(4*PERCENT_CHANGE))*(price)
    #print("Stop loss set at: " + str(stopLoss))
    takeProfit = (1+PERCENT_CHANGE)*(price)
    return balance, unitsAvailable, stopLoss, takeProfit

def ordinarySellMax(date, balance, price, unitsAvailable, display):
    qty = unitsAvailable
    if display:
        print(str(date) + ": SELL " + str(qty) + " units at $" + str(price))
    balance = balance + qty*price
    unitsAvailable = 0
    return balance, unitsAvailable

def stopLossSell(date, balance, price, unitsAvailable, display):
    qty = math.floor(UNORDINARY_SELL_PERCENT*unitsAvailable)
    if display:
        print(str(date) + ": STOP LOSS SELL " + str(qty) + " units at $" + str(price))
    balance = balance + qty*price
    unitsAvailable -= qty
    return balance, unitsAvailable

def takeProfitSell(date, balance, price, unitsAvailable, display):
    qty = math.floor(UNORDINARY_SELL_PERCENT*unitsAvailable)
    if display:
        print(str(date) + ": TAKE PROFITS SELL " + str(qty) + " units at $" + str(price))
    balance = balance + qty*price
    unitsAvailable -= qty
    return balance, unitsAvailable
