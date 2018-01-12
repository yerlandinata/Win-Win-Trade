class Order:

    def __init__(self, exchange, order_id, currency_pair, order_type, price, submit_time, amount, finish_time=None):
        self.exchange = exchange
        self.order_id = order_id
        self.currency_pair = currency_pair
        self.order_type = order_type
        self.price = price
        self.submit_time = submit_time
        self.amount = amount
        self.finish_time = finish_time
        self.is_canceled = False
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '<Order: {}>'.format(self.__dict__)

    def __hash__(self):
        return hash(self.__dict__)

    def is_fulfilled(self):
        self.refresh()
        return self.finish_time is not None

    def cancel(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()
