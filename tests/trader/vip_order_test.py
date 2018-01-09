import pytest
from src.trader import VipOrder
from src.exchange.exchange import ExchangeOperationFailedError

@pytest.fixture()
def exchange(mocker):
    return mocker.Mock()

def test_refresh(exchange):
    order = VipOrder(exchange, '1', 'btc_idr', 'buy', 1, 1, 2)
    exchange.get_order.return_value = VipOrder(exchange, '1', 'btcidr', 'buy', 1, 1, 0, finish_time=2)
    order.refresh()
    exchange.get_order.assert_called_once_with(order_id='1', currency_pair='btc_idr')
    assert order.finish_time == 2
    assert order.get_remaining() == 0
    assert order.is_fulfilled()

def test_cancel_success(exchange):
    order = VipOrder(exchange, '1', 'btc_idr', 'buy', 1, 1, 2)
    order.cancel()
    assert order.is_canceled
    exchange.cancel_order.assert_called_once_with(order_id='1', currency_pair='btc_idr', order_type='buy')

def test_cancel_failed(exchange):
    order = VipOrder(exchange, '1', 'btc_idr', 'buy', 1, 1, 2)
    fail_message = 'aaa'
    exchange.cancel_order.side_effect = ExchangeOperationFailedError(fail_message)
    with pytest.raises(ExchangeOperationFailedError) as excinfo:
        order.cancel()
    assert fail_message == str(excinfo.value)
