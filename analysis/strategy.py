import pandas as pd, numpy as np

from util.market import MARKET_MODE

_ABS_CHANGE_LOWER_THRESHOLD = 0.1
_ABS_CHANGE_UPPER_THRESHOLD = 0.2
_TIME_WINDOW_BACKWARD_MINUTES = 10
_TIME_WINDOW_FORWARD_MINUTES_DROP = 5
_TIME_WINDOW_FORWARD_MINUTES_JUMP = 5
_DROP_CHANGE_THRESHOLD = -0.1
_JUMP_CHANGE_THRESHOLD = 0.1

class Parameters:
    def __init__(self):
        abs_change_lower_threshold = _ABS_CHANGE_LOWER_THRESHOLD
        abs_change_upper_threshold = _ABS_CHANGE_UPPER_THRESHOLD
        time_window_backward_minutes = _TIME_WINDOW_BACKWARD_MINUTES
        time_window_forward_drop_minutes = _TIME_WINDOW_FORWARD_MINUTES_DROP
        time_window_forward_jump_minutes = _TIME_WINDOW_FORWARD_MINUTES_JUMP
        drop_change_threshold = _DROP_CHANGE_THRESHOLD
        jump_change_threshold = _JUMP_CHANGE_THRESHOLD
        long_on_jump = True
        self.abs_change_lower_threshold = abs_change_lower_threshold
        self.abs_change_upper_threshold = abs_change_upper_threshold
        self.time_window_backward_minutes = time_window_backward_minutes
        self.time_window_forward_drop_minutes = time_window_forward_drop_minutes
        self.time_window_forward_jump_minutes = time_window_forward_jump_minutes
        self.drop_change_threshold = drop_change_threshold
        self.jump_change_threshold = jump_change_threshold
        self.long_on_jump = long_on_jump

    def __str__(self):
        return '''
abs_change_lower_threshold: {abs_change_lower_threshold}, 
abs_change_upper_threshold: {abs_change_upper_threshold},
time_window_backward_minutes: {time_window_backward_minutes}, 
time_window_forward_drop_minutes: {time_window_forward_drop_minutes},
time_window_forward_jump_minutes: {time_window_forward_jump_minutes},
long_on_jump: {long_on_jump}
        '''.format(
            abs_change_lower_threshold=self.abs_change_lower_threshold,
            abs_change_upper_threshold=self.abs_change_upper_threshold,
            time_window_backward_minutes=self.time_window_backward_minutes,
            time_window_forward_drop_minutes=self.time_window_forward_drop_minutes,
            time_window_forward_jump_minutes=self.time_window_forward_jump_minutes,
            long_on_jump=self.long_on_jump
        )

    def get_feature_backward(self):
        return 'close_change_b_{w}_w{w}'.format(w=self.time_window_backward_minutes)

    def get_feature_forward_drop(self):
        return 'close_change_f_{w}_w{w}'.format(w=self.time_window_forward_drop_minutes)

    def get_feature_forward_jump(self):
        return 'close_change_f_{w}_w{w}'.format(w=self.time_window_forward_jump_minutes)

def _dedupe_consecutives(df_signal, parameter):
    df_signal_by_symbol = df_signal.reset_index().set_index('symbol').sort_index(by=['symbol', 'datetime'])
    df_signal_by_symbol['datetime'] = df_signal_by_symbol['datetime'].astype('datetime64[ns]')

    #df_signal_by_symbol = df_signal_by_symbol[
    #    df_signal_by_symbol.datetime.diff().fillna(np.timedelta64(100, 'm')) > np.timedelta64(parameter.time_window_backward_minutes, 'm')]

    #df_signal_by_symbol = df_signal_by_symbol[df_signal_by_symbol.datetime.diff().fillna(np.timedelta64(100, 'm')) > np.timedelta64(parameter.time_window_backward_minutes, 'm')]

    df_signal_by_symbol = df_signal_by_symbol[
        df_signal_by_symbol.datetime.diff(-1).fillna(np.timedelta64(-100, 'm')) < -np.timedelta64(parameter.time_window_backward_minutes, 'm')]

    df_signal_deduped = df_signal_by_symbol.reset_index().set_index(['datetime', 'symbol'])
    return df_signal_deduped

def pick_signal(dff, parameter):
    time_window_backward_minutes = parameter.time_window_backward_minutes
    feature_backward = parameter.get_feature_backward()
    feature_backward_2 = 'close_change_b_{window2}_w{window}'.format(window2=time_window_backward_minutes * 2,
                                                                     window=time_window_backward_minutes)
    feature_forward_drop = parameter.get_feature_forward_drop()

    df_signal = dff

    df_signal = df_signal[np.abs(df_signal[feature_backward]) > parameter.abs_change_lower_threshold]
    df_signal = df_signal[np.abs(df_signal[feature_backward]) < parameter.abs_change_upper_threshold]
    # df_signal = df_signal[np.abs(df_signal[feature_backward_2]) < 0.10]
    # dff = dff[dff[feature_backward] < -0.10]
    df_signal = df_signal[(df_signal[feature_backward] > parameter.jump_change_threshold) | (df_signal[feature_backward] < parameter.drop_change_threshold)]

    df_signal_deduped = _dedupe_consecutives(df_signal, parameter)

    return df_signal_deduped



