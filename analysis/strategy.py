import pandas as pd, numpy as np

from util.market import MARKET_MODE

_DAILY_CHANGE_LOWER_LIMIT_KOR = 0.13
_DAILY_CHANGE_UPPER_LIMIT_KOR = 0.3
_DAILY_CHANGE_LOWER_LIMIT_US = 0.07
_DAILY_CHANGE_UPPER_LIMIT_US = 0.2


class Parameters:
    def __init__(self, market_mode, feature_name):
        lower_limit, upper_limit = _DAILY_CHANGE_LOWER_LIMIT_KOR, _DAILY_CHANGE_UPPER_LIMIT_KOR
        if market_mode is MARKET_MODE.MARKET_KOR:
            lower_limit = _DAILY_CHANGE_LOWER_LIMIT_KOR
            upper_limit = _DAILY_CHANGE_UPPER_LIMIT_KOR
        elif market_mode is MARKET_MODE.MARKET_US:
            if feature_name == 'open_close':
                lower_limit = 0.05
                upper_limit = _DAILY_CHANGE_UPPER_LIMIT_US
            elif feature_name == 'close_close':
                lower_limit = 0.07
                upper_limit = _DAILY_CHANGE_UPPER_LIMIT_US
            elif feature_name == 'close_open':
                lower_limit = 0.09
                upper_limit = _DAILY_CHANGE_UPPER_LIMIT_US

            #lower_limit = _DAILY_CHANGE_LOWER_LIMIT_US
            #upper_limit = _DAILY_CHANGE_UPPER_LIMIT_US

        self.lower_limit, self.upper_limit = lower_limit, upper_limit

    def __str__(self):
        return "lower_limit: {lower_limit}, upper_limit: {upper_limit}".format(
            lower_limit=self.lower_limit,
            upper_limit=self.upper_limit)

def indicator_by_feature_kor(df, feature_name):
    '''
    indicator decides which symbols should be traded the next day
    :param df:
    :param feature_name:
    :param upper_limit:
    :param lower_limit:
    :return:
    '''
    print('by {column_name}'.format(column_name=feature_name))
    parameters = Parameters(MARKET_MODE.MARKET_KOR, feature_name)
    print('parameters')
    print(parameters)
    #df = df.loc[df['prev2_{column_name}'.format(column_name=column_name)] < consecutive_days_change_upper_limit]  # no consecutive jumps
    df = df.loc[df[feature_name +'_1'] < parameters.upper_limit]
    df = df.loc[df[feature_name +'_1'] > parameters.lower_limit]
    df = df.loc[df[feature_name + '_3'] < parameters.lower_limit]
    df = df.loc[df[feature_name + '_4'] < parameters.lower_limit]

    df = df.loc[df['close_open_1'] > -0.02]
    return df

def indicator_by_feature_us(df, feature_name):
    '''
    indicator decides which symbols should be traded the next day
    :param df:
    :param feature_name:
    :param upper_limit:
    :param lower_limit:
    :return:
    '''
    print('by {column_name}'.format(column_name=feature_name))
    parameters = Parameters(MARKET_MODE.MARKET_US, feature_name)
    print('parameters')
    print(parameters)
    #df = df.loc[df['prev2_{column_name}'.format(column_name=column_name)] < consecutive_days_change_upper_limit]  # no consecutive jumps
    df = df.loc[df[feature_name +'_1'] < parameters.upper_limit]
    df = df.loc[df[feature_name +'_1'] > parameters.lower_limit]
    df = df.loc[df[feature_name +'_2'] < parameters.upper_limit]
    df = df.loc[df[feature_name +'_2'] > parameters.lower_limit]
    df = df.loc[df[feature_name + '_3'] < 0.04]
    #df = df.loc[df[feature_name + '_4'] < lower_limit]
    #df = df.loc[df.volume_2 > df.volume_3]
    df = df.loc[df.volume_1 > 4000]

    df = df.loc[df['close_open_1'] > -0.02]
    return df

def indicator_by_feature(df, feature_name, market_mode):
    '''
    indicator decides which symbols should be traded the next day
    :param df:
    :param feature_name:
    :param upper_limit:
    :param lower_limit:
    :return:
    '''
    if market_mode is MARKET_MODE.MARKET_KOR:
        return indicator_by_feature_kor(df, feature_name)
    elif market_mode is MARKET_MODE.MARKET_US:
        return indicator_by_feature_us(df, feature_name)

debug_columns = ['open', 'close', 'open_close_1', 'close_open_1', 'close_close_1']

def print_profit_by_feature(df_by_feature):
    print('open_close(sum of daily mean):', np.sum(df_by_feature.groupby(level=0).open_close_0.mean()))
    print('close_open(sum of daily mean):', np.sum(df_by_feature.groupby(level=0).close_open_0.mean()))
    print('close_close(sum of daily mean):', np.sum(df_by_feature.groupby(level=0).close_close_0.mean()))
    print('closestopped_open(sum of daily mean):', np.sum(df_by_feature.groupby(level=0).closestopped_open_0.mean()))
    print('closestopped_close(sum of daily mean):', np.sum(df_by_feature.groupby(level=0).closestopped_close_0.mean()))
    print('')
    print('open_close(mean):', df_by_feature.open_close_0.mean())
    print('close_open(mean):', df_by_feature.close_open_0.mean())
    print('close_close(mean):', df_by_feature.close_close_0.mean())
    print('closestopped_open(mean):', df_by_feature.closestopped_open_0.mean())
    print('closestopped_close(mean):', df_by_feature.closestopped_close_0.mean())
    print('')
    print('mean number of the events on event day:', df_by_feature.groupby(level=0).close.count().mean())
    print('the number of the events:', len(df_by_feature))
    print('the number of the eventful days:', len(set(df_by_feature.index.get_level_values(0))))
    print('open_close(sum):', df_by_feature.open_close_0.sum())
    print('close_open(sum):', df_by_feature.close_open_0.sum())
    print('close_close(sum):', df_by_feature.close_close_0.sum())
    print('')
    print('open_close(std):', df_by_feature.open_close_0.std())
    print('close_open(std):', df_by_feature.close_open_0.std())
    print('close_close(std):', df_by_feature.close_close_0.std())

    df_daily_mean = df_by_feature.groupby(level=0)[['open_close_0', 'close_open_0', 'close_close_0']].mean().sort_index(ascending=False)
    print('')
