from datetime import datetime
from collections import OrderedDict
import requests
import pytest
from pytest_mock import mocker
from src.exchange.vip_exchange import VipExchangeAccount

@pytest.fixture()
def exchange():
    return VipExchangeAccount('a', 'b')

@pytest.fixture()
def req_mock(mocker, monkeypatch):
    mockery = mocker.Mock(return_value=mocker.Mock())
    mockery.return_value.content = '{"success": 1}'
    monkeypatch.setattr(requests, 'get', mockery)
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
