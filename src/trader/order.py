class Order:

    def __init__(self, exchange, order_id, currency_pair, order_type, price, submit_time, remaining_amount, finish_time=None):
        self.exchange = exchange
        self.order_id = order_id
        self.currency_pair = currency_pair
        self.order_type = order_type
        self.price = price
        self.submit_time = submit_time
        self.remaining_amount = remaining_amount
        self.finish_time = finish_time
        self.is_canceled = False
    
    def is_fulfilled(self):
        self.refresh()
        return self.remaining_amount == 0

    def get_remaining(self):
        self.refresh()
        return self.remaining_amount

    def cancel(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()
