from . import Order

class VipOrder(Order):

    def cancel(self):
        self.exchange.cancel_order(order_id=self.order_id, currency_pair=self.currency_pair, order_type=self.order_type)
        self.is_canceled = True

    def refresh(self):
        updated = self.exchange.get_order(order_id=self.order_id, currency_pair=self.currency_pair)
        self.finish_time = updated.finish_time
        self.remaining_amount = updated.remaining_amount
        