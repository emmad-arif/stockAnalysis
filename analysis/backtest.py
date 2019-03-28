import pullAndEnrich
import utilities as util
from scripts import plot as candlePlt
from scripts import simplePlot as simplePlt
import sys, os
from strategies import EMACrossover, SMACrossover, SMALSCrossover, RSI, randomStrategy
import datetime # linear

""" Check CLI Validity """
if len(sys.argv) < 2:
    file = open("backtestHelp.txt", "r")
    print (file.read())
    exit()

if "-h" in sys.argv or "-H" in sys.argv:
    file = open("backtestHelp.txt", "r")
    print (file.read())
    exit()


ticker = sys.argv[1][1:].upper()
enrichedPath = "data/enriched/" + ticker + ".enriched.csv"
rawPath = "data/raw/" + ticker + ".csv"

indicators = []
strategies = []
plotIndicators = False
plotBacktests = False
forcePull = False
display = False
randomStrategyCount = 10

""" Process command line arguments"""
for i in range(2, len(sys.argv)):
    arg = sys.argv[i].lower()

    if arg[0] != '-':
        continue
    arg = arg[1:]

    if arg == "smac":
        smaPeriod = sys.argv[i+1]
        strategies.append(arg + smaPeriod)
        indicators.append("sma" + smaPeriod)
        continue

    if arg == "emac":
        emaPeriod = sys.argv[i+1]
        strategies.append(arg + emaPeriod)
        indicators.append("ema" + emaPeriod)
        continue

    if arg == "smalsc":
        smaLongPeriod = sys.argv[i+1]
        smaShortPeriod = sys.argv[i+2]
        if int(smaLongPeriod) <= int(smaShortPeriod):
            print("Error: SMA Long Horizon must be longer than SMA Short Horizon")
            sys.stdout.flush()
            continue
        strategies.append(arg + smaLongPeriod + '-' + smaShortPeriod)
        indicators.append("sma" + smaLongPeriod)
        indicators.append("sma" + smaShortPeriod)
        continue

    if arg == "rsi":
        rsiPeriod = sys.argv[i+1]
        strategies.append("rsi" + rsiPeriod)
        indicators.append("rsi" + rsiPeriod)
        continue

    if arg == "plotbacktests" or arg == "plotbacktest":
        plotBacktests = True

    if arg == "plotindicators" or arg == "plotindicator":
        plotIndicators = True

    if arg == "display":
        display = True

    if arg == "forcepull":
        forcePull = True

""" Remove Duplicates from strategies and indicators """
indicators = util.removeDuplicates(indicators)
strategies = util.removeDuplicates(strategies)

if forcePull and os.path.isfile(rawPath):
    os.unlink(rawPath)

if os.path.isfile(enrichedPath):
    os.unlink(enrichedPath)

""" Pull and/or Enrich pricing data """
pullAndEnrich.pullAndEnrich(ticker, "full", rawPath, enrichedPath, indicators)


""" Backtest Random strategy """
util.printPartition()
print("Simulating Random Strategy " + str(randomStrategyCount) + " times.")
randomReturn = randomStrategy.runMultipleRandoms(enrichedPath, randomStrategyCount)
print("\nRandom strategy would have returned: " + str(randomReturn) + "% over a period of " + str(round(util.periods(enrichedPath)/365, 2)) + " years (on average).")
sys.stdout.flush()


""" Backtest each strategy requested """
for strategy in strategies:

    if "smac" in strategy:
        horizon = strategy[4:]
        util.printPartition()
        print("Simulating SMA Crossover Strategy with time horizon: " + horizon)
        sys.stdout.flush()
        buys, sells = SMACrossover.SMACrossover().runBacktest(enrichedPath, int(horizon), display)
        if plotBacktests:
            simplePlt.plot(ticker, enrichedPath, buys, sells, "SMA Crossover (" + horizon + " day) Strategy Backtest")

    elif "emac" in strategy:
        horizon = strategy[4:]
        util.printPartition()
        print("Simulating EMA Crossover Strategy with time horizon: " + horizon)
        sys.stdout.flush()
        buys, sells = EMACrossover.EMACrossover().runBacktest(enrichedPath, int(horizon), display)
        if plotBacktests:
            simplePlt.plot(ticker, enrichedPath, buys, sells, "EMA Crossover (" + horizon + " day) Strategy Backtest")

    elif "smalsc" in strategy:
        i = 0
        for letter in strategy:
            if letter == '-':
                break
            i += 1
        longHorizon = strategy[6:i]
        shortHorizon = strategy[i+1:]
        util.printPartition()
        print("Simulating SMA Long/Short Crossover Strategy with long time horizon: " + longHorizon + " and short time horizon: " + shortHorizon)
        sys.stdout.flush()
        buys, sells = SMALSCrossover.SMALSCrossover().runBacktest(enrichedPath, int(longHorizon), int(shortHorizon), display)
        if plotBacktests:
            simplePlt.plot(ticker, enrichedPath, buys, sells, "SMA Long/Short (" + longHorizon + "/" + shortHorizon + " day) Strategy Backtest")

    elif "rsi" in strategy:
        horizon = strategy[3:]
        util.printPartition()
        print("Simulating RSI Strategy")
        sys.stdout.flush()
        buys, sells = RSI.RSI().runBacktest(enrichedPath, int(horizon), display)
        if plotBacktests:
            simplePlt.plot(ticker, enrichedPath, buys, sells, "RSI (" + horizon + " day) Strategy Backtest")

""" Plot indicators used for strategies above """
if plotIndicators:
    candlePlt.plot(ticker, enrichedPath, indicators)
