from datetime import datetime
import requests
import pandas as pd
import json
from src.valid_pairs import *
from . import Market

class BitcoinIndonesiaMarket(Market):

    PAIRS = {
        BTCIDR: 'BTCIDR',
        ETHIDR: 'ETHIDR',
        BCHIDR: 'BCHIDR',
        BTGIDR: 'BTGIDR',
        XLMIDR: 'XLMIDR',
        XRPIDR: 'XRPIDR',
        NXTIDR: 'NXTIDR'
    }

    PAIRS_DEPTH = {
        BTCIDR: 'btc_idr',
        ETHIDR: 'eth_idr',
        BCHIDR: 'bch_idr',
        BTGIDR: 'btg_idr',
        XLMIDR: 'str_idr',
        XRPIDR: 'xrp_idr',
        NXTIDR: 'nxt_idr'
    }

    def __init__(self):
        super().__init__('https://vip.bitcoin.co.id', ohlc_endpoint='/tradingview/history')

    def parse_ohlc_data(self, json_text):
        j = json.loads(json_text)
        return pd.DataFrame(
            data={'open': j['o'], 'high': j['h'], 'low': j['l'], 'close': j['c'], 'volume': j['v']},
            index=j['t']
        )

    def get_ohlc(self, currency, after, before=None, period=1):
        if currency not in BitcoinIndonesiaMarket.PAIRS:
            raise RuntimeError('Invalid currency pair: ' + currency)
        if before is None:
            before = int(datetime.now().timestamp())
        query = {'symbol': BitcoinIndonesiaMarket.PAIRS[currency], 'from': str(after), 'to': str(before), 'resolution': str(period)}
        response = requests.get(self.ohlc_url, params=query)
        return self.parse_ohlc_data(response.content)

    def get_buy_order_book(self, currency):
        self.__depth_currency_check(currency)
        response = requests.get(self.base_url + '/api/' + BitcoinIndonesiaMarket.PAIRS_DEPTH[currency] + '/depth')
        d = json.loads(response.content)
        buy = {i: p for i, p in d['buy']}
        buying = []
        buy_price = list(buy.keys())
        buy_price.sort()
        for p in buy_price:
            buying.append(float(buy[p]))
        return pd.DataFrame(data={'buy': buying}, index=buy_price)

    def get_sell_order_book(self, currency):
        self.__depth_currency_check(currency)
        response = requests.get(self.base_url + '/api/' + BitcoinIndonesiaMarket.PAIRS_DEPTH[currency] + '/depth')
        d = json.loads(response.content)
        sell = {i: p for i, p in d['sell']}
        selling = []
        sell_price = list(sell.keys())
        sell_price.sort()
        for p in sell_price:
            selling.append(float(sell[p]))
        return pd.DataFrame(data={'sell': selling}, index=sell_price)

    def get_best_price(self, currency):
        depth_buy = self.get_buy_order_book(currency)
        depth_sell = self.get_sell_order_book(currency)
        return (depth_buy.tail(1).index[0] + depth_sell.head(1).index[0]) // 2

    def __depth_currency_check(self, currency):
        if currency not in BitcoinIndonesiaMarket.PAIRS_DEPTH:
            raise RuntimeError('Invalid currency pair: ' + currency)
