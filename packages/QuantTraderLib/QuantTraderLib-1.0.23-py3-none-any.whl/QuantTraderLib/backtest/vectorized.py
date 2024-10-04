import pandas as pd
from QuantTraderLib.backtest_source.source import Backtest, Strategy
from QuantTraderLib.backtest_source.lib import SignalStrategy, TrailingStrategy

def use_position(data, pos_array):
    """
    Use buy/sell signals from an array and perform backtest.

    Parameters:
        data (DataFrame): Data containing prices and signals.
        pos_array (array-like): Array containing buy/sell signals (1/-1).

    Returns:
        tuple: Statistics and results of the backtest.
    """

    class PosStrategy(Strategy):
        """
        Strategy using buy/sell signals for trading.
        """

        def init(self):
            pass
        
        def next(self):
            current_signal = self.data.Signal

            if current_signal == 1:
                if not self.position:
                    self.buy()       
            elif current_signal == -1:
                if self.position:
                    self.position.close()

    pos_array.index = data.index
    data['Signal'] = pos_array
    bt = Backtest(data, PosStrategy)
    stats = bt.run()
    return stats, bt

def use_signal_ma(data, ma1, ma2):
    """
    Use a strategy based on moving average signals and perform backtest.

    Parameters:
        data (DataFrame): Data containing prices and signals.
        ma1 (int): Time period for the first moving average of Close prices.
        ma2 (int): Time period for the second moving average of Close prices.

    Returns:
        stats (dict): Statistics of the test.
        bt (Backtest): Results of the test.
    """

    def SMA(arr: pd.Series, n: int) -> pd.Series:
        """
        Return the moving average time period of an array `arr`.
        """
        return pd.Series(arr).rolling(n).mean()

    class MASignal(SignalStrategy):
        """
        Strategy using moving average signals for trading.
        """
        def init(self):
            super().init()
            price = self.data.Close
            self.ma1 = self.I(SMA, price, ma1)
            self.ma2 = self.I(SMA, price, ma2)
            self.set_signal(self.ma1 > self.ma2, self.ma1 < self.ma2)
        
        def next(self):
            super().next()

    bt = Backtest(data, MASignal)
    stats = bt.run()
    return stats, bt

def use_trailing(data, atr_periods, trailing_sl, rolling):
    """
    Thực hiện kiểm thử chiến lược giao dịch sử dụng trailing stop-loss.
    
    Hàm này khởi tạo và chạy một kiểm thử giao dịch cho một chiến lược sử dụng trailing stop-loss.

    Tham số:
        data (DataFrame): Dữ liệu giá lịch sử bao gồm giá Open, High, Low, Close.
        atr_periods (int): Số kỳ tính toán Average True Range (ATR).
        trailing_sl (int): Kích thước trailing stop-loss theo đơn vị ATR.
        rolling (int): Số kỳ cho cửa sổ trượt.

    Trả về:
        stats (dict): Thống kê của kiểm thử.
        bt (Backtest): Hình vẽ của kiểm thử.
    """

    class SLTrailling(TrailingStrategy):
        """
        Chiến lược giao dịch mẫu sử dụng trailing stop-loss.
        """

        def init(self):
            """
            Khởi tạo các tham số chiến lược và chỉ báo.
            """
            super().init()
            self.set_atr_periods(atr_periods)
            self.set_trailing_sl(trailing_sl)
            self.sma = self.I(lambda: self.data.Close.s.rolling(rolling).mean())

        def next(self):
            """
            Thực hiện logic giao dịch trên mỗi điểm dữ liệu mới.
            """
            super().next()
            if not self.position and self.data.Close > self.sma:
                self.buy()

    # Khởi tạo và chạy kiểm thử
    bt = Backtest(data, SLTrailling)
    stats = bt.run()

    return stats, bt