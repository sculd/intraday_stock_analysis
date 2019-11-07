import pandas as pd, numpy as np
import util.time as util_time
from analysis import features, daily_pick
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
    filename = 'data/us.intraday.polygon.history.csv'
    df = pd.read_csv(filename, index_col=['time','symbol']).sort_index()

df = df.loc[~df.index.duplicated(keep='first')]
dff = features.add_features(df, market_mode=market_mode)

time_window_minutes = 15
feature_backward = 'close_change_b_{window}_w{window}'.format(window=time_window_minutes)
feature_forward = 'close_change_f_{window}_w{window}'.format(window=time_window_minutes)
dff = dff[dff[feature_backward] != 0][dff[feature_forward] != 0]

change_threshold = 0.10
dff = dff[np.abs(dff[feature_backward]) > change_threshold]
#dff = dff[dff[feature_backward] < -0.20]
#dff = dff[(dff[feature_backward] > 0.10) | (dff[feature_backward] < -0.10)]

print('')
print('time_window_minutes:', time_window_minutes)
print('change_threshold:', change_threshold)

print('')
print('number of events:', len(dff))

print('')
profit = dff[dff[feature_backward] < 0][feature_forward].sum()
profit += -dff[dff[feature_backward] > 0][feature_forward].sum()
print('projected return (long and short):', profit)

print('')
profit = dff[dff[feature_backward] < 0][feature_forward].sum()
print('projected return (long):', profit)

print('')
print(dff[[feature_backward, feature_forward]].corr())

print('')
print('outlying riser (>0.3)')
print(dff[dff[feature_forward] > 0.3][['close_b_10', 'close_b_5', 'close', 'close_f_5', 'close_f_10']])

image_file_name = 'images/time_window_minutes_{time_window_minutes}_{change_threshold}.png'.format(time_window_minutes=time_window_minutes, change_threshold=change_threshold)
plots.scatter.do_plot(
    dff[feature_backward], dff[feature_forward],
    xlabel='backward',
    ylabel='forward',
    image_file_name=image_file_name)

exit(0)
