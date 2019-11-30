import pandas as pd, numpy as np
import util.time as util_time
from analysis import features, strategy, evaluation
import plots.scatter
from util.market import MARKET_MODE
import config

market_mode = MARKET_MODE.MARKET_US

filename = None
df = None
if market_mode is MARKET_MODE.MARKET_KOR:
    filename = 'data/combined.2019-09-20.csv'
    df = pd.read_csv(filename, index_col=['datetime', 'symbol']).sort_index()
elif market_mode is MARKET_MODE.MARKET_US:
    #filename = 'data/us.intraday.polygon.history.csv'
    #df = pd.read_csv(filename, index_col=['time','symbol']).sort_index()
    filename = 'data/stream.minute.csv'
    df = pd.read_csv(filename, index_col=['datetime','symbol']).sort_index()

df = df.loc[~df.index.duplicated(keep='first')]
dff = features.add_features(df, market_mode=market_mode)

param = strategy.Parameters()
param.time_window_forward_drop_minutes = 15
param.time_window_forward_jump_minutes = 5
param.long_on_jump = False
param.change_lower_threshold = 0.10
df_signal = strategy.pick_signal(dff, param)

evaluation.print_evaluation(df_signal, param)


image_file_name = 'images/time_window_backward_minutes_{time_window_backward_minutes}_{change_lower_threshold}_drop.png'.format(time_window_backward_minutes=param.time_window_backward_minutes, change_lower_threshold=param.change_lower_threshold)
plots.scatter.do_plot(
    df_signal[param.get_feature_backward()], df_signal[param.get_feature_forward_drop()],
    xlabel='backward',
    ylabel='forward(drop)',
    image_file_name=image_file_name)

image_file_name = 'images/time_window_backward_minutes_{time_window_backward_minutes}_{change_lower_threshold}_jump.png'.format(time_window_backward_minutes=param.time_window_backward_minutes, change_lower_threshold=param.change_lower_threshold)
plots.scatter.do_plot(
    df_signal[param.get_feature_backward()], df_signal[param.get_feature_forward_jump()],
    xlabel='backward',
    ylabel='forward(jump)',
    image_file_name=image_file_name)

exit(0)
