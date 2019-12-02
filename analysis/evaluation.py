import numpy as np


def print_evaluation(df_signal, param):
    feature_backward = param.get_feature_backward()
    feature_forward_drop = param.get_feature_forward_drop()
    feature_forward_jump = param.get_feature_forward_jump()

    print('')
    print(param)

    print('')
    print('number of events:', len(df_signal))
    print('number of drop events:', len(df_signal[df_signal[feature_backward] < 0]))
    print('number of jump events:', len(df_signal[df_signal[feature_backward] > 0]))
    print('number of zero backward change over {w}'.format(w=param.time_window_backward_minutes), len(df_signal[df_signal[feature_backward] == 0]))
    print('number of zero forward change over {w}'.format(w=param.time_window_forward_drop_minutes), len(df_signal[df_signal[feature_forward_drop] == 0]))

    df_signal = df_signal[df_signal[feature_backward] != 0][df_signal[feature_forward_drop] != 0]
    profit_by_drop = df_signal[df_signal[feature_backward] < 0][feature_forward_drop].sum()

    jump_sign = 1 if param.long_on_jump else -1
    profit_by_jump = jump_sign * df_signal[df_signal[feature_backward] > 0][feature_forward_jump].sum()
    #profit_by_jump = df_signal[df_signal[feature_backward] > 0][feature_forward_jump].sum()

    profit = profit_by_drop + profit_by_jump

    print('')
    print('projected return longing drop:', profit_by_drop)

    print('')
    on_jump_str = 'longing' if param.long_on_jump else 'shorting'
    print('projected return {on_jump_str} jump:'.format(on_jump_str=on_jump_str), profit_by_jump)

    print('')
    print('projected return (drop and jump together):', profit)

    print('for drop')
    print(df_signal[[feature_backward, feature_forward_drop]].corr())

    print('for jump')
    print(df_signal[[feature_backward, feature_forward_jump]].corr())

    print('')
    print('outlying riser (>0.3)')
    print(df_signal[df_signal[feature_forward_jump] > 0.3][['close_b_10', 'close_b_5', 'close', 'close_f_5', 'close_f_10']])
