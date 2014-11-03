import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from my_sma_crossover import *

def parameters_generator():
    instrument = ["ivv"]
    entrySMA = range(5, 20)
    exitSMA = range(5, 20)
    return itertools.product(instrument, entrySMA, exitSMA)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Download the bars.
    feed = yahoofinance.build_feed(["ivv"], 2008, 2009, ".")
    local.run(SMACrossOver2, feed, parameters_generator())
