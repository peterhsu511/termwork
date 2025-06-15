# strategy/chart.py
import plotly.graph_objects as go
import pandas as pd


def KBar_to_df(KBar_dic):
    df = pd.DataFrame(KBar_dic)
    df.columns = [i.lower() for i in df.columns]
    df['time'] = pd.to_datetime(df['time'])
    return df


def plot_strategy(title, KBar_dic, TradeRecord, MA_long=None, MA_short=None):
    df = KBar_to_df(KBar_dic)

    fig = go.Figure()

    # K 線圖
    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='K線'))

    # 均線
    if MA_long and MA_long in df:
        fig.add_trace(go.Scatter(
            x=df['time'], y=df[MA_long],
            mode='lines', name='MA長期', line=dict(color='red')
        ))

    if MA_short and MA_short in df:
        fig.add_trace(go.Scatter(
            x=df['time'], y=df[MA_short],
            mode='lines', name='MA短期', line=dict(color='orange')
        ))

    # 交易點：多單進場 / 出場
    for r in TradeRecord:
        action, _, entry_time, _, exit_time, *_ = r
        if entry_time in df['time'].values:
            price = df.loc[df['time'] == entry_time, 'low'].values[0]
            fig.add_trace(go.Scatter(x=[entry_time], y=[price], mode='markers',
                                     marker=dict(symbol='triangle-up', color='green', size=12),
                                     name='多單進場'))
        if exit_time in df['time'].values:
            price = df.loc[df['time'] == exit_time, 'high'].values[0]
            fig.add_trace(go.Scatter(x=[exit_time], y=[price], mode='markers',
                                     marker=dict(symbol='triangle-down', color='blue', size=12),
                                     name='多單出場'))

    fig.update_layout(title=title, xaxis_title='時間', yaxis_title='價格',
                      xaxis_rangeslider_visible=False, template='plotly_white')

    fig.show()
