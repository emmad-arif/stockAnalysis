import pullAndEnrich
import utilities as util
from scripts import plot as plt
import predict, sys, os
from strategies import EMACrossover, SMACrossover, smaLSC, RSI, LinearRegression, randomStrategy
import datetime # linear
import pandas as pd
import config
if len(sys.argv) < 2:
    file = open("adviceHelp.txt", "r")
    print (file.read())
    exit()

if "-h" in sys.argv or "-H" in sys.argv:
    file = open("adviceHelp.txt", "r")
    print (file.read())
    exit()


ticker = sys.argv[1][1:].upper()
enrichedPath = "data/enriched/" + ticker + ".enriched.csv"
rawPath = "data/raw/" + ticker + ".csv"

#indicators = ["sma5", "sma20", "sma200", "emac5", "rsi"]
#strategies = ["smac5", "emac5", "smalsc200-20", "rsi"]
SMACWindow = 5
EMACWindow = 5
LRWindow = 2
RSIWindow = 14 # NEED TO IMPLEMENT ALTERNATE ENRICHMENT LOGIC
nextNDays = 10
indicators = ["rsi", "sma5", "ema5"]
#strategies = ["rsi"]
plot = False
forcePull = False


if forcePull and os.path.isfile(rawPath):
    os.unlink(rawPath)

if os.path.isfile(enrichedPath):
    os.unlink(enrichedPath)

""" Pull and/or Enrich pricing data """
pullAndEnrich.pullAndEnrich(ticker, "full", rawPath, enrichedPath, indicators)
df = pd.read_csv(enrichedPath)

print("\nBased on the close price on " + df.iloc[len(df) - 1]['timestamp'] + ":")



""" Run RSI """

strat = RSI.RSI()
result = strat.heuristic(df)
historicAccuracy = strat.historicAccuracy(df, nextNDays)
#print(str(rsiResult))

if result >= 0.7:
    print("\n" + str(RSIWindow) + " day RSI is suggesting an *upward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult-0.5)/0.5) + "% confident " + ticker + " stock will go up soon.")
elif result <= 0.3:
    print("\n" + str(RSIWindow) + " day RSI is suggesting *downward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult)/0.5) + "% confident " + ticker + " stock will go down soon.")
else:
    print("RSI is uncertain...")
print("RSI has historically been " + str(historicAccuracy) + "% accurate in predicting a " + str(config.PERCENT_CHANGE*100) + "% change (at least) for " + ticker + " stock over " + str(nextNDays) + " days.")
sys.stdout.flush()

""" Run SMA Crossover """


strat = SMACrossover.SMACrossover()
result = strat.heuristic(df, SMACWindow)
historicAccuracy = strat.historicAccuracy(df, SMACWindow, nextNDays)


if result >= 0.7:
    print("\n" + str(SMACWindow) + " day SMA Crossover is suggesting an *upward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult-0.5)/0.5) + "% confident " + ticker + " stock will go up soon.")
elif result <= 0.3:
    print("\n" + str(SMACWindow) + " day SMA Crossover is suggesting a *downward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult)/0.5) + "% confident " + ticker + " stock will go down soon.")
else:
    print("\n" + str(SMACWindow) + " day SMA Crossover is uncertain...")
print(str(SMACWindow) + " day SMA Crossover has historically been " + str(historicAccuracy) + "% accurate in predicting a " + str(config.PERCENT_CHANGE*100) + "% change (at least) for " + ticker + " stock over " + str(nextNDays) + " days.")
sys.stdout.flush()

""" Run EMA Crossover """

strat = EMACrossover.EMACrossover()
result = strat.heuristic(df, EMACWindow)
historicAccuracy = strat.historicAccuracy(df, EMACWindow, nextNDays)


if result >= 0.7:
    print("\n" + str(EMACWindow) + " day EMA Crossover is suggesting an *upward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult-0.5)/0.5) + "% confident " + ticker + " stock will go up soon.")
elif result <= 0.3:
    print("\n" + str(EMACWindow) + " day EMA Crossover is suggesting a *downward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult)/0.5) + "% confident " + ticker + " stock will go down soon.")
else:
    print("\n" + str(EMACWindow) + " day EMA Crossover is uncertain...")
print(str(EMACWindow) + " day EMA Crossover has historically been " + str(historicAccuracy) + "% accurate in predicting a " + str(config.PERCENT_CHANGE*100) + "% change (at least) for " + ticker + " stock over " + str(nextNDays) + " days.")
sys.stdout.flush()

""" Run Linear Regression """

strat = LinearRegression.LinearRegression()
result = strat.heuristic(df, LRWindow)
historicAccuracy = strat.historicAccuracy(df, LRWindow, nextNDays)


if result == 1:
    print("\n" + str(LRWindow) + " day Linear Regression is suggesting an *upward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult-0.5)/0.5) + "% confident " + ticker + " stock will go up soon.")
elif result == 0:
    print("\n" + str(LRWindow) + " day Linear Regression is suggesting a *downward* move (relative to today's price) within the next " + str(nextNDays) + " days.")
    #print("\nRSI is " + str(100*(rsiResult)/0.5) + "% confident " + ticker + " stock will go down soon.")
else:
    print("\n" + str(LRWindow) + " day Linear Regression is uncertain...")
print(str(LRWindow) + " day Linear Regression has historically been " + str(historicAccuracy) + "% accurate in predicting a " + str(config.PERCENT_CHANGE*100) + "% change (at least) for " + ticker + " stock over " + str(nextNDays) + " days.")
sys.stdout.flush()

if plot:
    plt.plot(ticker, enrichedPath, indicators)

exit()
