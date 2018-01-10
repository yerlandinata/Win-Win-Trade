from pandas import DataFrame

class Indicator:

    def __init__(self, init_data):
        '''
        init_data must be pandas.DataFrame object with structure:
        timestamp (index)   |   open    |   high    |   low     |   close   |   volume  |
        int                     float       float       float       float       float
        '''
        self.data = init_data
        self.size = len(self.data)

    def update(self, timestamp, _open, high, low, close, volume):
        tail_df = DataFrame(data={
            'open': [_open],
            'high': [high],
            'low': [low],
            'close': [close],
            'volume': [volume]
        }, index=[timestamp])
        self.data = self.data.append(tail_df)
        self.data = self.data.tail(self.size)

    def is_buy_signal(self, *args, **kwargs):
        raise NotImplementedError()

    def is_sell_signal(self, *args, **kwargs):
        raise NotImplementedError()
