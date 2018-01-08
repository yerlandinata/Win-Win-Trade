from datetime import datetime
from collections import OrderedDict
import requests
import pytest
from pytest_mock import mocker
from src.exchange.exchange import ExchangeOperationFailedError
from src.exchange.vip_exchange import VipExchangeAccount
from src.trader.vip_order import VipOrder

@pytest.fixture()
def exchange():
    return VipExchangeAccount('a', 'b')

@pytest.fixture()
def req_mock(mocker, monkeypatch):
    mockery = mocker.Mock(return_value=mocker.Mock())
    mockery.return_value.content = '{"success": 1}'
    monkeypatch.setattr(requests, 'post', mockery)
    return mockery

def test_calculate_signature(exchange):
    '''
    Expecting signature based on the secret key defined in exchange()
    '''
    payload = OrderedDict([
        ('nonce', '1515258126'),
        ('method', 'getInfo')
    ])
    expected_signature = '450b244834e0896d1f5d5429511e18d660b4f600f18513dade9196779e54f49ac990a7b86ec9027035c7f69bc88df188e33baf255adf38f428a697f8a496042e'
    assert exchange.calculate_signature(payload) == expected_signature

def test_post_request(exchange, req_mock):
    expected_headers = {
        'Key': 'a',
        'Sign': '450b244834e0896d1f5d5429511e18d660b4f600f18513dade9196779e54f49ac990a7b86ec9027035c7f69bc88df188e33baf255adf38f428a697f8a496042e'
    }
    payload = OrderedDict([
        ('nonce', '1515258126'),
        ('method', 'getInfo')
    ])
    assert exchange.post_request(payload) == {'success': 1}
    req_mock.assert_called_once_with(VipExchangeAccount.BASE_URL, data=payload, headers=expected_headers)

def test_get_balance(exchange, req_mock):
    currencies = ['idr', 'btc', 'ltc', 'doge']
    expects = [10000, 3.14, 33.14, 1600.299]
    req_mock.return_value.content = '{"success":1,"return":{"balance":{"idr":10000,"btc":3.14,"ltc":33.14,"doge":1600.299},"server_time":1392225342}}'
    for currency, expect in zip(currencies, expects):
        assert exchange.get_balance(currency) == expect
        args, kwargs = req_mock.call_args
        assert args[0] == VipExchangeAccount.BASE_URL
        assert kwargs['data'] == OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'getInfo')
        ])
    assert req_mock.call_count == len(currencies)

def test_get_order_with_id(exchange, req_mock):
    pair = 'ltc_idr'
    order_id = '94425'
    req_mock.return_value.content = '{"success": 1,"return": {"order": {"order_id": "94425","price": "0.00810000","type": "sell","order_ltc": "1.00000000","remain_ltc": "0.53000000","submit_time": "1497657065","finish_time": "0","status": "open"}}}'
    expected = VipOrder(exchange, order_id, 'ltc_idr', 'sell', 0.0081, 1497657065, 0.53)
    actual_test = exchange.get_order(order_id=order_id, currency_pair=pair)
    assert actual_test == expected
    args, kwargs = req_mock.call_args
    assert args[0] == VipExchangeAccount.BASE_URL
    assert kwargs['data'] == OrderedDict([
        ('nonce', str(int(datetime.now().timestamp()))),
        ('method', 'getOrder'),
        ('pair', pair),
        ('order_id', order_id)
    ])

def test_get_order_with_id_fail(exchange, req_mock):
    pair = 'ltc_idr'
    order_id = '94425'
    req_mock.return_value.content = '{"success": 0, "error": "some error"}'
    with pytest.raises(ExchangeOperationFailedError) as excinfo:
        exchange.get_order(order_id=order_id, currency_pair=pair)
    assert str(excinfo.value) == 'some error'
