from pandas import DataFrame

class Indicator:

    def __init__(self, init_data):
        '''
        init_data must be pandas.DataFrame object with structure:
        timestamp (index)   |   open    |   high    |   low     |   close   |   volume  |
        int                     float       float       float       float       float
        '''
        self.data = init_data
        self.interval = len(self.data)

    def update(self, timestamp, _open, high, low, close, volume):
        tail_df = DataFrame(data={
            'open': [_open],
            'high': [high],
            'low': [low],
            'close': [close],
            'volume': [volume]
        }, index=[timestamp])
        self.data = self.data.append(tail_df)
        self.data = self.data.tail(self.interval)

    def is_buy_signal(self):
        raise NotImplementedError()

    def is_sell_signal(self):
        raise NotImplementedError()
