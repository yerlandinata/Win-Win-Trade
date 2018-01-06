from datetime import datetime
import hmac
import hashlib
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
        q = urlencode(payload)
        m = bytes(q, 'utf-8')
        return hmac.new(self.__secret, msg=m, digestmod=hashlib.sha512).hexdigest()

    def post_request(self, payload, signature):
        pass

    def get_balance(self):
        pass

    def get_order(self, currency, order_id=None):
        pass

    def is_order_fulfilled(self, currency, order_id):
        pass

    def place_buy_order(self, currency_pair, amount):
        pass

    def place_sell_order(self, currency_pair, amount):
        pass
