from datetime import datetime
import hmac
import hashlib
import json
from collections import OrderedDict
from urllib.parse import urlencode
import requests
from .base import ExchangeAccount

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
        pass

    def get_order(self, currency, order_id=None):
        pass

    def is_order_fulfilled(self, currency, order_id):
        pass

    def place_buy_order(self, currency_pair, amount):
        pass

    def place_sell_order(self, currency_pair, amount):
        pass
