import math
# Returns new balance and units available

stopLossCutoff = 0.95
stopLossPct = 1.00

def ordinaryBuyMax(date, balance, price, unitsAvailable, type="", printTrades=True):
    qty = math.floor(balance/price)
    #print(type(date))
    print(str(date) + ": BUY " + str(qty) + " units at $" + str(price))
    balance = balance - qty*price
    unitsAvailable += qty
    stopLoss = stopLossCutoff*(price)
    return balance, unitsAvailable, stopLoss

def ordinarySellMax(date, balance, price, unitsAvailable, type="", printTrades=True):
    qty = unitsAvailable
    print(str(date) + ": SELL " + str(qty) + " units at $" + str(price))
    balance = balance + qty*price
    unitsAvailable = 0
    return balance, unitsAvailable

def stopLossSell(date, balance, price, unitsAvailable, type="", printTrades=True):
    qty = math.floor(stopLossPct*unitsAvailable)
    print(str(date) + ": STOP LOSS SELL " + str(qty) + " units at $" + str(price))
    balance = balance + qty*price
    unitsAvailable -= qty
    return balance, unitsAvailable
