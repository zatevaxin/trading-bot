import math

import talib as ta
from chart import Chart

from strategies.strategybase import StrategyBase

MAIN_PERIOD = 50
SIGNAL_PERIOD = 3


class Strategy(StrategyBase):
    __strategy__ = 'scalpinator'

    def __init__(self, args, chart: 'Chart', exchange, mode, budget):
        super().__init__(args, chart, exchange, mode, budget)

    def tick(self) -> dict:
        candle = self.get_current_candle()

        close = self.indicators.close_array

        sma = ta.SMA(ta.SMA(close, math.ceil(MAIN_PERIOD / 2)), math.floor(MAIN_PERIOD / 2) + 1)
        signal_line = ta.SMA(close, SIGNAL_PERIOD)

        scalping_line = signal_line - sma

        if all((scalping_line > 0)[-3:]):
            self.open_trade(stop_loss_percent=1.0)

        if all((scalping_line < 0)[-2:]):
            self.close_trade()

        return {"scalping-line": scalping_line}

    def rt_tick(self, candle: 'Candle') -> dict:

        return {}
