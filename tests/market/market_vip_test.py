from datetime import datetime
import requests
import pytest
from pytest_mock import mocker
from src.market.market_vip import BitcoinIndonesiaMarket

@pytest.fixture()
def market():
    return BitcoinIndonesiaMarket()

@pytest.fixture()
def req_mock(mocker, monkeypatch):
    mockery = mocker.Mock(return_value=mocker.Mock())
    mockery.return_value.content = '{"s":"mock","t":[],"o":"mock","h":"mock","l":"mock","c":"mock","v":"mock"}'
    monkeypatch.setattr(requests, 'get', mockery)
    return mockery

def test_get_ohlc_with_before_url(market, req_mock):
    symbol = 'BTCIDR'
    before = 2
    after = 1
    expected_query = {'symbol': symbol, 'from': str(after), 'to': str(before), 'resolution':'1'}
    market.get_ohlc(symbol, after, before=before)
    req_mock.assert_called_once_with('https://vip.bitcoin.co.id/tradingview/history', params=expected_query)

def test_get_ohlc_without_before_url(market, req_mock):
    symbol = 'BTCIDR'
    before = int(datetime.now().timestamp())
    after = 1
    expected_query = {'symbol': symbol, 'from': str(after), 'to': str(before), 'resolution':'1'}
    market.get_ohlc(symbol, after)
    req_mock.assert_called_once_with('https://vip.bitcoin.co.id/tradingview/history', params=expected_query)

def test_parse_ohlc_data(market):
    json_str = '{\
        "s":"ok",\
        "t":[1514861100,1514862000,1514862900,1514863800,1514864700,1514865600,1514866500,1514867400,1514868300,1514869200],\
        "c":[217998000,216999000,215845000,215999000,215337000,216541000,215985000,214964000,214850000,215105000],\
        "o":[217084000,217998000,216999000,215845000,215999000,215337000,216541000,215985000,214964000,214850000],\
        "h":[217998000,218400000,217000000,215999000,216392000,217500000,217397000,215985000,214980000,215184000],\
        "l":[217006000,216900000,215000000,215251000,214017000,215000000,215100000,214151000,214202000,214849000],\
        "v":[3.18698879,6.82663246,15.68406076,2.15531776,12.87793266,7.0219555,4.56684082,7.37273228,8.14764141,3.09377636]\
    }'
    price = market.parse_ohlc_data(json_str)
    assert list(price.index) == [1514861100, 1514862000, 1514862900, 1514863800, 1514864700, 1514865600, 1514866500, 1514867400, 1514868300, 1514869200]
    assert list(price.open) == [217084000, 217998000, 216999000, 215845000, 215999000, 215337000, 216541000, 215985000, 214964000, 214850000]
    assert list(price.high) == [217998000, 218400000, 217000000, 215999000, 216392000, 217500000, 217397000, 215985000, 214980000, 215184000]
    assert list(price.low) == [217006000, 216900000, 215000000, 215251000, 214017000, 215000000, 215100000, 214151000, 214202000, 214849000] 
    assert list(price.close) == [217998000, 216999000, 215845000, 215999000, 215337000, 216541000, 215985000, 214964000, 214850000, 215105000]
    assert list(price.volume) == [3.18698879, 6.82663246, 15.68406076, 2.15531776, 12.87793266, 7.0219555, 4.56684082, 7.37273228, 8.14764141, 3.09377636]
