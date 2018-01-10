from . import Indicator

class EMACrossoverIndicator(Indicator):

    def __init__(self, init_data, short_period, long_period, confirm_period=0):
        if len(init_data) != long_period + confirm_period:
            raise RuntimeError('Inconsistent data size with configuration. \
            Data size is {}, the configuration requires the data size to be equal to\
             long_period + confirm_period = {}'.format(len(init_data), long_period + confirm_period))
        super().__init__(init_data)
        self.short_period = short_period
        self.long_period = long_period
        self.confirm_period = confirm_period

    def is_sell_signal(self, *args, **kwargs):
        count = 0
        for val in self.__ema_cross():
            if val < 0:
                count += 1
            else: count = 0
        return count >= self.confirm_period

    def is_buy_signal(self, *args, **kwargs):
        count = 0
        for val in self.__ema_cross():
            if val > 0:
                count += 1
            else: count = 0
        return count >= self.confirm_period

    def __ema_cross(self):
        ema_short = self.data.close.ewm(span=self.short_period, min_periods=self.short_period).mean()
        ema_long = self.data.close.ewm(span=self.long_period, min_periods=self.long_period).mean()
        return ema_short - ema_long
