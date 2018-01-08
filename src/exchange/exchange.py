class ExchangeAccount:

    def get_balance(self, currency):
        raise NotImplementedError()

    def get_order(self, **kwargs):
        raise NotImplementedError()

    def cancel_order(self, **kwargs):
        raise NotImplementedError()

    def place_buy_order(self, **kwargs):
        raise NotImplementedError()

    def place_sell_order(self, **kwargs):
        raise NotImplementedError()

class ExchangeOperationFailedError(RuntimeError):
    pass
