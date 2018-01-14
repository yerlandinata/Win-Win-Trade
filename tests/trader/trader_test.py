from datetime import datetime, timedelta
import pytest
from pandas import DataFrame
from src.valid_pairs import *
from src.trader import Trader, Order

@pytest.fixture()
def exchange(mocker):
    return mocker.Mock()

@pytest.fixture()
def indicator(mocker):
    return mocker.Mock()

@pytest.fixture()
def market(mocker):
    return mocker.Mock()

def test_update_indicator(exchange, market, indicator):
    trader = Trader(BTCIDR, exchange, market, indicator, 50000, price_period=15)
    market.get_ohlc.return_value = DataFrame(data={
        'open': [10],
        'high': [12],
        'low': [8],
        'close': [11],
        'volume': [2]
    }, index=[127])
    trader.update_indicator()
    market.get_ohlc.assert_called_once_with(BTCIDR, int((datetime.now() - timedelta(minutes=15)).timestamp()), period=15)
    indicator.update.assert_called_once_with(127, 10, 12, 8, 11, 2)

def test_take_action_buy_wait_buy_signal(exchange, market, indicator):
    invest = 50000
    trader = Trader(BTCIDR, exchange, market, indicator, invest)
    indicator.is_buy_signal.return_value = True
    price = 10
    market.get_best_price.return_value = price
    order = Order(exchange, 1, BTCIDR, 'buy', price, 1, 1)
    exchange.place_buy_order.return_value = order
    trader.take_action()
    indicator.is_buy_signal.assert_called_once()
    market.get_best_price.assert_called_once()
    exchange.place_buy_order.assert_called_once_with(currency_pair=BTCIDR, price=price, amount=invest)
    assert trader.state == Trader.BUYING
  
def test_take_action_buy_wait_no_buy_signal(exchange, market, indicator):
    invest = 50000
    trader = Trader(BTCIDR, exchange, market, indicator, invest)
    indicator.is_buy_signal.return_value = False
    trader.take_action()
    indicator.is_buy_signal.assert_called_once()
    market.get_best_price.assert_not_called()
    exchange.place_buy_order.assert_not_called()
    assert trader.state == Trader.BUY_WAIT

def test_take_action_sell_wait_sell_signal(exchange, market, indicator):
    invest = 1
    coin = 0.5
    trader = Trader(BTCIDR, exchange, market, indicator, invest)
    trader.state = Trader.SELL_WAIT
    trader.coin = coin
    indicator.is_sell_signal.return_value = True
    price = 10
    market.get_best_price.return_value = price
    order = Order(exchange, 1, BTCIDR, 'sell', price, 1, coin)
    exchange.place_sell_order.return_value = order
    trader.take_action()
    indicator.is_sell_signal.assert_called_once()
    market.get_best_price.assert_called_once()
    exchange.place_sell_order.assert_called_once_with(currency_pair=BTCIDR, price=price, amount=coin)
    assert trader.state == Trader.SELLING
    
def test_manage_order_buy_success(mocker, exchange, market, indicator):
    order = mocker.Mock()
    order.is_fulfilled.return_value = True
    order.amount = 5
    order.price = 20
    order.order_type = 'buy'
    exchange.get_order_fee.return_value = 100
    trader = Trader(BTCIDR, exchange, market, indicator, 1)
    trader.state = Trader.BUYING
    trader.orders.append(order)
    trader.fee_paid = 50
    trader.manage_orders()
    assert trader.coin == 100
    assert trader.state == Trader.SELL_WAIT
    assert trader.fee_paid == 150
    exchange.get_order_fee.assert_called_once_with(order=order)
    
def test_manage_order_buy_not_complete(mocker, exchange, market, indicator):
    order = mocker.Mock()
    order.is_fulfilled.return_value = False
    order.amount = 5
    order.order_type = 'buy'
    trader = Trader(BTCIDR, exchange, market, indicator, 1)
    trader.state = Trader.BUYING
    trader.orders.append(order)
    trader.manage_orders()
    assert trader.state == Trader.BUYING
    assert trader.coin == 0
    exchange.get_order_fee.assert_not_called()
    
def test_manage_order_sell_success(mocker, exchange, market, indicator):
    order = mocker.Mock()
    order.is_fulfilled.return_value = True
    order.amount = 100000
    order.order_type = 'sell'
    exchange.get_order_fee.return_value = 200
    trader = Trader(BTCIDR, exchange, market, indicator, 50000)
    trader.state = Trader.SELLING
    trader.orders.append(order)
    trader.fee_paid = 50
    trader.manage_orders()
    assert trader.coin == 0
    assert trader.investment == 100000
    assert trader.state == Trader.BUY_WAIT
    assert trader.fee_paid == 250
    exchange.get_order_fee.assert_called_once_with(order=order)
    
def test_manage_order_sell_not_complete(mocker, exchange, market, indicator):
    order = mocker.Mock()
    order.is_fulfilled.return_value = False
    order.amount = 5
    order.order_type = 'sell'
    indicator.is_sell_signal.return_value = False
    trader = Trader(BTCIDR, exchange, market, indicator, 1)
    trader.state = Trader.SELLING
    trader.orders.append(order)
    trader.manage_orders()
    assert trader.state == Trader.SELLING
    exchange.get_order_fee.assert_not_called()

def test_manage_order_handle_market_crashing(mocker, exchange, market, indicator):
    order = mocker.Mock()
    order.is_fulfilled.return_value = False
    order.amount = 5
    order.order_type = 'sell'
    indicator.is_sell_signal.return_value = True
    price = 10
    market.get_best_price.return_value = price
    remaining_coin = 4
    order_new = Order(exchange, 5, BTCIDR, 'sell', price, 12, remaining_coin)
    exchange.get_balance.return_value = remaining_coin
    exchange.place_sell_order.return_value = order_new
    exchange.get_order_fee.return_value = 20
    trader = Trader(BTCIDR, exchange, market, indicator, 1)
    trader.state = Trader.SELLING
    trader.orders.append(order)
    trader.coin = 5
    trader.fee_paid = 5
    trader.manage_orders()
    order.cancel.assert_called_once()
    indicator.is_sell_signal.assert_called()
    market.get_best_price.assert_called_once()
    exchange.get_balance.assert_called_once_with('btc')
    exchange.get_order_fee.assert_called_once_with(order=order)
    exchange.place_sell_order.assert_called_once_with(currency_pair=BTCIDR, price=price, amount=remaining_coin)
    assert trader.state == Trader.SELLING
    assert trader.coin == remaining_coin
    assert trader.orders[-1] == order_new
    assert trader.fee_paid == 25
