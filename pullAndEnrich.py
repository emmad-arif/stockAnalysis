from scripts import pullData, sma

pullData.pull("MSFT")
sma.appendSMA("MSFT", 5)
