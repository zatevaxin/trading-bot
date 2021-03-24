import math

import talib as ta
from chart import Chart

from strategies.strategybase import StrategyBase

MAIN_PERIOD = 100
SIGNAL_PERIOD = 7


class Strategy(StrategyBase):
    __strategy__ = 'scalper.1.0'

    def __init__(self, chart: 'Chart', exchange, mode, budget):
        super().__init__(chart, exchange, mode, budget)

    def tick(self) -> dict:
        candle = self.get_current_candle()

        close = self.indicators.close_array

        sma = ta.SMA(ta.SMA(close, math.ceil(MAIN_PERIOD / 2)), math.floor(MAIN_PERIOD / 2) + 1)
        signal_line = ta.SMA(close, SIGNAL_PERIOD)

        scalping_line = signal_line - close

        current_rsi = self.indicators.rsi_array[-1]

        if all((scalping_line > 0)[-3:]) and (scalping_line[-2] < scalping_line[-1]
                                              or scalping_line[-3] < scalping_line[-1]):
            if current_rsi <= 50:
                self.open_trade(candle, stop_loss_percent=1.0)

        if all((scalping_line < 0)[-2:]) and (scalping_line[-2] >= scalping_line[-1]
                                              or scalping_line[-3] >= scalping_line[-1]):
            self.close_trade(candle)

        return {"scalping-line": scalping_line}
