import numpy as np


def print_evaluation(df_signal, param):
    feature_backward = param.get_feature_backward()
    feature_forward_drop = param.get_feature_forward_drop()
    feature_forward_jump= param.get_feature_forward_jump()

    print('')
    print('time_window_minutes_backward:', param.time_window_minutes)
    print('time_window_forward_drop_minutes:', param.time_window_forward_drop_minutes)
    print('time_window_forward_jump_minutes:', param.time_window_forward_jump_minutes)
    print('change_lower_threshold:', param.change_lower_threshold)
    print('change_upper_threshold:', param.change_upper_threshold)

    print('')
    print('number of events:', len(df_signal))

    profit_by_drop = df_signal[df_signal[feature_backward] < 0][feature_forward_drop].sum()

    #profit_short = -df_signal[df_signal[feature_backward] > 0][feature_forward_jump].sum()
    profit_by_jump = df_signal[df_signal[feature_backward] > 0][feature_forward_jump].sum()

    profit = profit_by_drop + profit_by_jump

    print('')
    print('projected return (drop and jump):', profit)

    print('')
    print('projected return, longing drop:', profit_by_drop)

    print('')
    print('projected return longing jump:', profit_by_jump)

    print('for drop')
    print(df_signal[[feature_backward, feature_forward_drop]].corr())

    print('for jump')
    print(df_signal[[feature_backward, feature_forward_jump]].corr())

    print('')
    print('outlying riser (>0.3)')
    print(df_signal[df_signal[feature_forward_jump] > 0.3][['close_b_10', 'close_b_5', 'close', 'close_f_5', 'close_f_10']])

