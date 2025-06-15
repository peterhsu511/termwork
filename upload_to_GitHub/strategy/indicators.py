# strategy/indicators.py
import pandas as pd
import pandas_ta as ta


def add_MA(df, short_period=5, long_period=20):
    df['MA_short'] = ta.sma(df['close'], length=short_period)
    df['MA_long'] = ta.sma(df['close'], length=long_period)
    return df


def add_RSI(df, period=14):
    df['RSI'] = ta.rsi(df['close'], length=period)
    return df


def add_Bollinger_Bands(df, period=20, nbdev=2):
    bb = ta.bbands(df['close'], length=period, std=nbdev)
    df['BB_upper'] = bb[f'BBU_{period}_{nbdev}.0']
    df['BB_middle'] = bb[f'BBM_{period}_{nbdev}.0']
    df['BB_lower'] = bb[f'BBL_{period}_{nbdev}.0']
    return df


def add_MACD(df, fastperiod=12, slowperiod=26, signalperiod=9):
    macd = ta.macd(df['close'], fast=fastperiod, slow=slowperiod, signal=signalperiod)
    df['MACD'] = macd[f'MACD_{fastperiod}_{slowperiod}_{signalperiod}']
    df['MACD_signal'] = macd[f'MACDs_{fastperiod}_{slowperiod}_{signalperiod}']
    df['MACD_hist'] = macd[f'MACDh_{fastperiod}_{slowperiod}_{signalperiod}']
    return df
