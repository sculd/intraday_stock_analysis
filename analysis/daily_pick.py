from analysis import strategy, features
import matplotlib.pyplot as plt
import pandas as pd
from util.market import MARKET_MODE

def _plot(df_by_feature, feature_name):
    df_plot = df_by_feature.groupby(level=0)[[feature_name + '_0']].mean().sort_index(ascending=False)
    df_plot.plot().get_figure().savefig('plots/{feature_name}.png'.format(feature_name=feature_name))

def _pick_today(df, feature_name, date_str, market_mode):
    consecutive_days_change_upper_limit = 0.08

    df_by_feature = strategy.indicator_by_feature(df, feature_name, market_mode)
    strategy.print_profit_by_feature(df_by_feature)
    _plot(df_by_feature, feature_name)

    debug_columns = [feature_name + '_0', 'closestopped_close_0'] + [feature_name + '_1']

    print('')
    print('mean by date')
    print(df_by_feature.groupby(level=0)[debug_columns].mean().sort_index(ascending=False).head(20))
    print('')
    print('sum by date')
    print(df_by_feature.groupby(level=0)[debug_columns].sum().sort_index(ascending=False).head(20))
    print(df_by_feature[debug_columns].sort_index(ascending=False).head(55))
    print(df_by_feature[debug_columns].sort_index(ascending=False).head(90).tail(35))

    return df_by_feature.xs(date_str, level=0) if date_str in df_by_feature.index else pd.DataFrame()

def pick_today(df, feature_name, date_str, market_mode=MARKET_MODE.MARKET_KOR):
    df = df.loc[~df.index.duplicated(keep='first')]
    df = features.add_features(df, market_mode=market_mode)
    df_by_feature = _pick_today(df, feature_name, date_str, market_mode)
    return df_by_feature

