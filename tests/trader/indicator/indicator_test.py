from pandas import DataFrame
from src.trader.indicator import Indicator

def test_update():
    df = DataFrame(data={
        'open': [i for i in range(5, 15)],
        'high': [i for i in range(10, 20)],
        'low': [i for i in range(10)],
        'close': [i for i in range(5, 15)],
        'volume': [i for i in range(1025, 1035)]
    }, index=[i for i in range(20, 30)])
    indicator = Indicator(df)
    indicator.update(30, 15, 20, 10, 15, 1035)
    expected_df = DataFrame(data={
        'open': [i for i in range(6, 16)],
        'high': [i for i in range(11, 21)],
        'low': [i for i in range(1, 11)],
        'close': [i for i in range(6, 16)],
        'volume': [i for i in range(1026, 1036)]
    }, index=[i for i in range(21, 31)])
    assert indicator.data.equals(expected_df)
