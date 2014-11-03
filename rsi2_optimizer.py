import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
import rsi2

def parameters_generator():
    instrument = ["dia"]
    entrySMA = range(150, 251)
    exitSMA = range(5, 16)
    rsiPeriod = range(2, 11)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(5, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Download the bars.
    feed = yahoofinance.build_feed(["dia"], 2009, 2011, ".")
    local.run(rsi2.RSI2, feed, parameters_generator())
