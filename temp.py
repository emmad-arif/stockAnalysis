import pullAndEnrich
import utilities as util
from scripts import plot
import predict

import datetime
ticker = "TSLA"
ticker = ticker.upper()
size = "full"
cutDate = "2010-01-01"
date = datetime.datetime.strptime(cutDate, '%Y-%m-%d').date()

##########################################################################################3
pullAndEnrich.pullAndEnrich(ticker, size, "data/raw/", "data/enriched/", "sma20", "ema20")
path = "data/enriched/" + ticker + ".enriched.csv"
util.cutCsv(path, date)


predict.smaCrossover(path, 20)
#plot.plot(path, "sma5", "ema5")
