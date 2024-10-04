from QuantTraderLib.backtest_source.source import Backtest, Strategy

def use_changes(data, changes):
    """
    Use strategy based on price changes and perform backtest.

    Parameters:
        data (DataFrame): Data containing prices.

    Returns:
        tuple: Statistics and backtest results.
    """
    class ChangesStrategy(Strategy):
        """
        Strategy using price changes for trading.

        """

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Changes

            if current_signal > 0:
                if not self.position:
                    self.buy()  
            elif current_signal < 0:
                if self.position:
                    self.position.close()

    data['Changes'] = changes 
    bt = Backtest(data, ChangesStrategy, exclusive_orders=True)
    stats = bt.run()
    return stats, bt
