import os
import time
import traceback
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
from src.log import logger
from src.exchange import VipExchangeAccount
from src.market import BitcoinIndonesiaMarket
from src.trader import Trader
from src.trader.indicator import EMACrossoverIndicator

def initialize():
    load_dotenv(find_dotenv())
    vip_api_key = os.environ.get('vip_api_key')
    vip_api_secret = os.environ.get('vip_api_secret')
    vip_trades_symbol = os.environ.get('vip_trades_symbol')
    initial_investment = os.environ.get('initial_investment')
    exchange_account = VipExchangeAccount(vip_api_key, vip_api_secret)
    market = BitcoinIndonesiaMarket()
    ema_crossorver_35_50_10 = EMACrossoverIndicator(market.get_ohlc(
        vip_trades_symbol, int((datetime.now() - timedelta(minutes=15*60)).timestamp()), period=15
    ), 35, 50, confirm_period=10)
    trader = Trader(vip_trades_symbol, exchange_account, market, ema_crossorver_35_50_10, 
                    initial_investment, price_period=15)
    begin_tick(trader)

def begin_tick(trader):
    while True:
        try:
            trader.tick()
            sleep_time = 60
            if trader.state == Trader.BUY_WAIT or trader.state == Trader.SELL_WAIT:
                sleep_time = 15 * 60
            time.sleep(sleep_time)
        except Exception as ex:
            end_tick(ex)

def end_tick(error):
    print(error)
    print('Details:')
    traceback.print_exc()
    print()
    print('Trading bot is stopped due to failures at', logger.time())
    while True:
        pass

print('Trading Bot initialized at ', logger.time())
initialize()
