import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def do_plot(df_1, df_2, xlabel='df1', ylabel='df2', image_file_name=None):
    # Create data
    N = 500

    # Plot
    plt.scatter(df_1, df_2, alpha=0.5)
    plt.title('Scatter plot')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.ylim([-0.15, 0.15])
    image_file_name = image_file_name or "images/scatter.png"
    plt.savefig(image_file_name)
    plt.show()

def plot(df, daily_change_lower_limit):
    df_daily_summary = pd.DataFrame()
    trade_by_column_name = 'close_close'
    df_daily_summary['daily_profit'] = df[df[trade_by_column_name + '_1'] > daily_change_lower_limit].groupby(level=0).open_close_1.sum()
    df_daily_summary['signal_length'] = df[df[trade_by_column_name + '_1'] > daily_change_lower_limit].groupby(level=0).close.count()
    print(df_daily_summary[['daily_profit', 'signal_length']].corr())
    print(df_daily_summary[df_daily_summary.signal_length >= 9].tail(20))

    do_plot(df_daily_summary.signal_length, df_daily_summary.daily_profit, xlabel='signal_length', ylabel='daily_profit')
