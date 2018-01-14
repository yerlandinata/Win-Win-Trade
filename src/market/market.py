class Market:

    def __init__(self, base_url, ohlc_endpoint=None, buy_orderbook_endpoint=None, sell_orderbook_endpoint=None):
        self.base_url = base_url
        self.ohlc_url = (self.base_url + ohlc_endpoint) if ohlc_endpoint else None
        self.buy_orderbook_url = (self.base_url + buy_orderbook_endpoint) if buy_orderbook_endpoint else None
        self.sell_orderbook_url = (self.base_url + sell_orderbook_endpoint) if sell_orderbook_endpoint else None

    def get_ohlc(self, currency, after, before=None, period='1'):
        raise NotImplementedError()

    def get_buy_order_book(self, currency):
        raise NotImplementedError()

    def get_sell_order_book(self, currency):
        raise NotImplementedError()

    def get_best_price(self, currency):
        raise NotImplementedError()

    def parse_ohlc_data(self, json_text):
        raise NotImplementedError()

class MarketDownError(RuntimeError):
    pass
