import pandas as pd, numpy as np

from util.market import MARKET_MODE

_CHANGE_LOWER_THRESHOLD = 0.1
_CHANGE_UPPER_THRESHOLD = 0.2
_TIME_WINDOW_MINUTES = 10
_TIME_WINDOW_FORWARD_MINUTES_DROP = 5
_TIME_WINDOW_FORWARD_MINUTES_JUMP = 10

class Parameters:
    def __init__(self):
        change_lower_threshold = _CHANGE_LOWER_THRESHOLD
        change_upper_threshold = _CHANGE_UPPER_THRESHOLD
        time_window_minutes = _TIME_WINDOW_MINUTES
        time_window_forward_drop_minutes = _TIME_WINDOW_FORWARD_MINUTES_DROP
        time_window_forward_jump_minutes = _TIME_WINDOW_FORWARD_MINUTES_JUMP
        self.change_lower_threshold = change_lower_threshold
        self.change_upper_threshold = change_upper_threshold
        self.time_window_minutes = time_window_minutes
        self.time_window_forward_drop_minutes = time_window_forward_drop_minutes
        self.time_window_forward_jump_minutes = time_window_forward_jump_minutes

    def __str__(self):
        return '''
        change_lower_threshold: {change_lower_threshold}, 
        change_upper_threshold: {change_upper_threshold},
        time_window_minutes: {time_window_minutes}, 
        time_window_forward_drop_minutes: {time_window_forward_drop_minutes},
        time_window_forward_jump_minutes: {time_window_forward_jump_minutes}
        '''.format(
            change_lower_threshold=self.change_lower_threshold,
            change_upper_threshold=self.change_upper_threshold,
            time_window_minutes=self.time_window_minutes,
            time_window_forward_drop_minutes=self.time_window_forward_drop_minutes,
            time_window_forward_jump_minutes=self.time_window_forward_jump_minutes
        )

    def get_feature_backward(self):
        return 'close_change_b_{w}_w{w}'.format(w=self.time_window_minutes)

    def get_feature_forward_drop(self):
        return 'close_change_f_{w}_w{w}'.format(w=self.time_window_forward_drop_minutes)

    def get_feature_forward_jump(self):
        return 'close_change_f_{w}_w{w}'.format(w=self.time_window_forward_jump_minutes)

def pick_signal(dff, parameter):
    time_window_minutes = parameter.time_window_minutes
    feature_backward = parameter.get_feature_backward()
    feature_backward_2 = 'close_change_b_{window2}_w{window}'.format(window2=time_window_minutes * 2,
                                                                     window=time_window_minutes)
    feature_forward_drop = parameter.get_feature_forward_drop()

    df_signal = dff[dff[feature_backward] != 0][dff[feature_forward_drop] != 0]

    df_signal = df_signal[np.abs(df_signal[feature_backward]) > parameter.change_lower_threshold]
    df_signal = df_signal[np.abs(df_signal[feature_backward]) < parameter.change_upper_threshold]
    df_signal = df_signal[np.abs(df_signal[feature_backward_2]) < 0.10]
    # dff = dff[dff[feature_backward] < -0.20]
    # dff = dff[(dff[feature_backward] > 0.10) | (dff[feature_backward] < -0.10)]

    return df_signal
