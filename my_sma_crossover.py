from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe, returns

class SMACrossOver2(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod, exit_sma_period):
        strategy.BacktestingStrategy.__init__(self, feed, 10000)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__exit_sma = ma.SMA(self.__prices, exit_sma_period)

    def getSMA(self):
        return self.__sma
    
    def get_exit_SMA(self):
        return self.__exit_sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__exit_sma) > 0:
            self.__position.exitMarket()

def main(plot, instrument, entry_sma_period, exit_sma_period):
    # Download the bars.
    feed = yahoofinance.build_feed([instrument], 2014, 2014, ".")
    
    strat = SMACrossOver2(feed, instrument, entry_sma_period, exit_sma_period)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

    strat.run()
    print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)

    if plot:
        plt.plot()

def main2(plot, instrument, entry_sma_period, exit_sma_period):
    # Download the bars.
    feed = yahoofinance.build_feed([instrument], 2014, 2014, ".")
    
    # Evaluate the strategy with the feed's bars.
    strat = SMACrossOver2(feed, instrument, entry_sma_period, exit_sma_period)
    
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)
    
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(strat)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot(instrument).addDataSeries("SMA", strat.getSMA())
    plt.getInstrumentSubplot(instrument).addDataSeries("exit SMA", strat.get_exit_SMA())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
    
    # Run the strategy.
    strat.run()
    strat.info("Final portfolio value: $%.2f" % strat.getResult())
    
    # Plot the strategy.
    plt.plot()

if __name__ == "__main__":
    instrument = "ivv"
    entry_sma_period = 20
    exit_sma_period = 10
    main(True, instrument, entry_sma_period, exit_sma_period)
    main2(True, instrument, entry_sma_period, exit_sma_period)
