from datetime import datetime, timedelta, timezone

def time():
    utc7 = timezone(timedelta(hours=7), name='UTC+7')
    return datetime.now(utc7).strftime('%d %m %Y - %H.%M')

def log_order_issue(order):
    print('[{}] {} order issued, id: {}, currency pair: {}, amount: {}, price: {}'
          .format(time(), order.order_type, order.order_id,
                  order.currency_pair, order.amount, order.price))

def log_order_canceled(order):
    print('[{}] {} order canceled, id: {}, currency pair: {}, amount: {}, price: {}'
          .format(time(), order.order_type, order.order_id,
                  order.currency_pair, order.amount, order.price))

def log_order_fulfilled(order):
    print('[{}] {} order fulfilled, id: {}, currency pair: {}, amount: {}, price: {}'
          .format(time(), order.order_type, order.order_id,
                  order.currency_pair, order.amount, order.price))

def log_investment(currency, amount):
    print('[{}] Investment value: {} {}'.format(time(), amount, currency))
