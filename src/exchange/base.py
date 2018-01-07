class ExchangeAccount:

    def get_balance(self, currency):
        pass

    def get_order(self, currency, order_id=None):
        pass

    def is_order_fulfilled(self, currency, order_id):
        pass

    def place_buy_order(self, currency_pair, amount):
        pass

    def place_sell_order(self, currency_pair, amount):
        pass
