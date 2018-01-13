from datetime import datetime, timedelta

class Trader:

    BUY_WAIT = 0
    BUYING = 1
    SELL_WAIT = 2
    SELLING = 3

    def __init__(self, currency_pair, exchange_account, market, indicator, initial_investment, price_period=15):
        self.currency_pair = currency_pair
        self.exchange_account = exchange_account
        self.market = market
        self.indicator = indicator
        self.investment = initial_investment
        self.coin = 0
        self.price_period = price_period
        self.state = Trader.BUY_WAIT
        self.orders = []
        self.fee_paid = 0

    def tick(self):
        self.update_indicator()
        if self.state == Trader.BUY_WAIT or self.state == Trader.SELL_WAIT:
            self.take_action()
        else: self.manage_orders()

    def update_indicator(self):
        recent_price = self.market.get_ohlc(
            self.currency_pair, int((datetime.now() - timedelta(minutes=self.price_period)).timestamp()), period=self.price_period
        ).tail(1)
        i = recent_price.index[0]
        self.indicator.update(recent_price.index[0], recent_price.open[i], recent_price.high[i],
                            recent_price.low[i], recent_price.close[i], recent_price.volume[i])

    def take_action(self):
        if self.state == Trader.BUY_WAIT:
            if self.indicator.is_buy_signal():
                price = self.market.get_best_price()
                self.orders.append(self.exchange_account.place_buy_order(currency_pair=self.currency_pair, price=price, amount=self.investment))
                self.state = Trader.BUYING
        elif self.state == Trader.SELL_WAIT:
            if self.indicator.is_sell_signal():
                price = self.market.get_best_price()
                self.orders.append(self.exchange_account.place_sell_order(currency_pair=self.currency_pair, price=price, amount=self.investment))
                self.state = Trader.SELLING

    def manage_orders(self):
        current_order = self.orders[-1]
        if current_order.order_type == 'buy':
            if current_order.is_fulfilled():
                self.coin = current_order.amount
                self.fee_paid += self.exchange_account.get_order_fee(order=current_order)
                self.state = Trader.SELL_WAIT
        elif current_order.order_type == 'sell':
            if current_order.is_fulfilled():
                self.coin = 0
                self.investment = current_order.amount
                self.fee_paid += self.exchange_account.get_order_fee(order=current_order)
                self.state = Trader.BUY_WAIT
            # TODO: Handle market crash
