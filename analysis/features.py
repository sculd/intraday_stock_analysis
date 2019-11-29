import pandas as pd, numpy as np

from util.market import MARKET_MODE

_CLOSE_LOWER_LIMIT_KRW = 2000
_CLOSE_LOWER_LIMIT_USD = 2
_PREV_VOLUME_LOWER_LIMIT = 3
_PREV_VOLUME_UPPER_LIMIT = 10000

def add_features(df, market_mode=MARKET_MODE.MARKET_KOR):
    close_lower_limit = None

    if market_mode is MARKET_MODE.MARKET_US:
        close_lower_limit = _CLOSE_LOWER_LIMIT_USD
    elif market_mode is MARKET_MODE.MARKET_KOR:
        close_lower_limit = _CLOSE_LOWER_LIMIT_KRW

    _diff_sign = 1

    df['close_b_0'] = df.close
    df['volume_b_0'] = df.volume
    df['close_f_0'] = df.close
    df['volume_f_0'] = df.volume
    for i in range(5, 36, 5):
        df['close_b_{i}'.format(i=i)] = df.groupby(level=1).shift(_diff_sign * i).close
        df['volume_b_{i}'.format(i=i)] = df.groupby(level=1).shift(_diff_sign * i).volume
        df['close_f_{i}'.format(i=i)] = df.groupby(level=1).shift(-1 * _diff_sign * i).close
        df['volume_f_{i}'.format(i=i)] = df.groupby(level=1).shift(-1 * _diff_sign * i).volume

    for window_size in range(5, 16, 5):
        for i in range(window_size, 36, 5):
            close_cur = df['close_b_{i}'.format(i=i-window_size)]
            close_prev = df['close_b_{i}'.format(i=i)]
            df['close_change_b_{i}_w{window_size}'.format(i=i, window_size=window_size)] = (close_cur - close_prev) / close_prev

        close_cur = df['close_f_{i}'.format(i=window_size)]
        close_prev = df['close_f_0']
        df['close_change_f_{w}_w{w}'.format(w=window_size)] = (close_cur - close_prev) / close_prev


    df = df[df.open != 0]
    df = df[df.close > close_lower_limit]

    df = df.dropna()
    return df
