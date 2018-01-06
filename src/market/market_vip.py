from datetime import datetime
import requests
import pandas as pd
import json
from .market import Market

class BitcoinIndonesiaMarket(Market):

    def __init__(self):
        super().__init__('https://vip.bitcoin.co.id', ohlc_endpoint='/tradingview/history')

    def parse_ohlc_data(self, json_text):
        j = json.loads(json_text)
        return pd.DataFrame(
            data={'open': j['o'], 'high': j['h'], 'low': j['l'], 'close': j['c'], 'volume': j['v']},
            index=j['t']
        )

    def get_ohlc(self, currency, after, before=None, period=1):
        if before is None:
            before = int(datetime.now().timestamp())
        query = {'symbol': currency, 'from': str(after), 'to': str(before), 'resolution': str(period)}
        response = requests.get(self.ohlc_url, params=query)
        return self.parse_ohlc_data(response.content)
