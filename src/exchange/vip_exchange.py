from datetime import datetime
import time
import hmac
import hashlib
import json
from collections import OrderedDict
from urllib.parse import urlencode
import requests
from src.valid_pairs import *
from src.trader import VipOrder
from . import ExchangeAccount, ExchangeOperationFailedError

class VipExchangeAccount(ExchangeAccount):

    BASE_URL = 'https://vip.bitcoin.co.id/tapi'
    PAIRS = {
        BTCIDR: 'btc_idr',
        ETHIDR: 'eth_idr',
        BCHIDR: 'bch_idr',
        BTGIDR: 'btg_idr',
        XLMIDR: 'xlm_idr',
        XRPIDR: 'xrp_idr',
        NXTIDR: 'nxt_idr'
    }
    INV_PAIRS = {v: k for k, v in PAIRS.items()}

    def __init__(self, api_key, secret):
        self.__api_key = api_key
        self.__secret = bytes(secret, 'utf-8')

    def get_balance(self, currency):
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'getInfo')
        ])
        res = self.post_request(payload)
        return res['return']['balance'][currency]

    def get_order(self, **kwargs):
        '''
        Arguments:
        order_id, currency_pair
        '''
        if kwargs['currency_pair'] not in VipExchangeAccount.PAIRS:
            raise RuntimeError('Invalid currency pair: ' + kwargs['currency_pair'])
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'getOrder'),
            ('pair', VipExchangeAccount.PAIRS[kwargs['currency_pair']]),
            ('order_id', kwargs['order_id'])
        ])
        res = self.post_request(payload)
        remain_key = ''
        for key in res['return']['order'].keys():
            if 'order' in key and key != 'order_id':
                remain_key = key
                break
        return VipOrder(self, str(kwargs['order_id']), kwargs['currency_pair'], res['return']['order']['type'],
                        float(res['return']['order']['price']), int(res['return']['order']['submit_time']),
                        float(res['return']['order'][remain_key]), finish_time=int(res['return']['order']['finish_time']) if int(res['return']['order']['finish_time']) else None)

    def get_order_fee(self, **kwargs):
        '''
        Arguments:
        order
        '''
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'tradeHistory'),
            ('pair', VipExchangeAccount.PAIRS[kwargs['order'].currency_pair]),
            ('order_id', kwargs['order'].order_id),
            ('count', 10)
        ])
        res = self.post_request(payload)
        for trade in res['return']['trades']:
            if kwargs['order'].order_id == trade['order_id']:
                return int(trade['fee'])

    def cancel_order(self, **kwargs):
        '''
        Arguments:
        order
        '''
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'cancelOrder'),
            ('pair', VipExchangeAccount.PAIRS[kwargs['order'].currency_pair]),
            ('order_id', kwargs['order'].order_id),
            ('type', 'buy')
        ])
        self.post_request(payload)

    def place_buy_order(self, **kwargs):
        '''
        Arguments:
        currency_pair, price, amount
        '''
        if kwargs['currency_pair'] not in VipExchangeAccount.PAIRS:
            raise RuntimeError('Invalid currency pair: ' + kwargs['currency_pair'])
        return self.__place_order(kwargs['currency_pair'], VipExchangeAccount.PAIRS[kwargs['currency_pair']].split('_')[1],
                                  'buy', kwargs['price'], kwargs['amount'])

    def place_sell_order(self, **kwargs):
        '''
        Arguments:
        currency_pair, price, amount
        '''
        if kwargs['currency_pair'] not in VipExchangeAccount.PAIRS:
            raise RuntimeError('Invalid currency pair: ' + kwargs['currency_pair'])
        return self.__place_order(kwargs['currency_pair'], VipExchangeAccount.PAIRS[kwargs['currency_pair']].split('_')[0],
                                  'sell', kwargs['price'], kwargs['amount'])

    def __place_order(self, currency_pair, currency_ask, order_type, price, amount):
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'trade'),
            ('pair', VipExchangeAccount.PAIRS[currency_pair]),
            ('type', order_type),
            ('price', price),
            (currency_ask, amount)
        ])
        res = self.post_request(payload)
        return self.get_order(order_id=res['return']['order_id'], currency_pair=currency_pair)

    def calculate_signature(self, payload):
        query = urlencode(payload)
        message = bytes(query, 'utf-8')
        return hmac.new(self.__secret, msg=message, digestmod=hashlib.sha512).hexdigest()

    def post_request(self, payload):
        header = {
            'Key': self.__api_key,
            'Sign': self.calculate_signature(payload)
        }
        res = requests.post(self.BASE_URL, data=payload, headers=header)
        time.sleep(1) # so there is no extra effort to work the nonce when there are too many requests at same time
        response_json = json.loads(res.content)
        self.__error_check(response_json)
        return response_json

    def __error_check(self, response):
        if response['success'] != 1:
            if 'error' in response.keys():
                raise ExchangeOperationFailedError(response['error'])
            else: raise ExchangeOperationFailedError('Unknown error')
