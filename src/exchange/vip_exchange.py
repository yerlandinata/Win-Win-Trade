from datetime import datetime
import hmac
import hashlib
import json
from collections import OrderedDict
from urllib.parse import urlencode
import requests
from src.trader import VipOrder
from . import ExchangeAccount, ExchangeOperationFailedError

class VipExchangeAccount(ExchangeAccount):

    BASE_URL = 'https://vip.bitcoin.co.id/tapi'

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
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'getOrder'),
            ('pair', kwargs['currency_pair']),
            ('order_id', kwargs['order_id'])
        ])
        res = self.post_request(payload)
        if res['success'] != 1:
            if 'error' in res.keys():
                raise ExchangeOperationFailedError(res['error'])
            else: raise ExchangeOperationFailedError('Unknown error')
        remain_key = ''
        for key in res['return']['order'].keys():
            if 'remain' in key:
                remain_key = key
                break
        return VipOrder(self, str(kwargs['order_id']), kwargs['currency_pair'], res['return']['order']['type'],
                        float(res['return']['order']['price']), int(res['return']['order']['submit_time']),
                        float(res['return']['order'][remain_key]), finish_time=int(res['return']['order']['finish_time']) if int(res['return']['order']['finish_time']) else None)

    def place_buy_order(self, **kwargs):
        '''
        Arguments:
        currency_pair, price, amount
        '''
        return self.__place_order(kwargs['currency_pair'], kwargs['currency_pair'].split('_')[0],
                                  'buy', kwargs['price'], kwargs['amount'])

    def place_sell_order(self, **kwargs):
        '''
        Arguments:
        currency_pair, price, amount
        '''
        return self.__place_order(kwargs['currency_pair'], kwargs['currency_pair'].split('_')[1],
                                  'sell', kwargs['price'], kwargs['amount'])

    def __place_order(self, currency_pair, currency_ask, order_type, price, amount):
        payload = OrderedDict([
            ('nonce', str(int(datetime.now().timestamp()))),
            ('method', 'trade'),
            ('pair', currency_pair),
            ('type', order_type),
            ('price', str(price)),
            (currency_ask, str(amount))
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
        return json.loads(res.content)
