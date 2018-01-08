from datetime import datetime
import hmac
import hashlib
import json
from collections import OrderedDict
from urllib.parse import urlencode
import requests
from .exchange import ExchangeAccount, ExchangeOperationFailedError
from src.trader.vip_order import VipOrder

class VipExchangeAccount(ExchangeAccount):

    BASE_URL = 'https://vip.bitcoin.co.id/tapi'

    def __init__(self, api_key, secret):
        self.__api_key = api_key
        self.__secret = bytes(secret, 'utf-8')

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
        return VipOrder(self, kwargs['order_id'], kwargs['currency_pair'], res['return']['order']['type'], 
                        float(res['return']['order']['price']), int(res['return']['order']['submit_time']), 
                        float(res['return']['order'][remain_key]), finish_time=int(res['return']['order']['finish_time']) if int(res['return']['order']['finish_time']) else None)

    def cancel_order(self, **kwargs):
        pass

    def place_buy_order(self, **kwargs):
        pass

    def place_sell_order(self, **kwargs):
        pass
