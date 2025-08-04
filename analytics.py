import pandas as pd
import plotly.graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression

def get_candlestick_data(df):
    df = df.copy()
    df['open'] = df['price'].shift(1).fillna(df['price'])
    df['high'] = df['price'].rolling(2).max()
    df['low'] = df['price'].rolling(2).min()
    df['close'] = df['price']
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def get_prediction_chart(df):
    df = df.copy()
    df['predicted'] = df['price'].rolling(window=10, min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], name='Actual'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['predicted'], name='Predicted'))
    fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)")
    return fig

def get_future_prediction_chart(df, days_ahead=3):
    df = df.copy().reset_index(drop=True)
    df['time_idx'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds() / 3600  # hours since start
    X = df['time_idx'].values.reshape(-1, 1)
    y = df['price'].values

    model = LinearRegression()
    model.fit(X, y)

    last_time = df['time_idx'].iloc[-1]
    future_hours = np.arange(last_time + 1, last_time + 73)  # next 72 hours
    future_timestamps = [df['timestamp'].iloc[-1] + pd.Timedelta(hours=int(h - last_time)) for h in future_hours]
    future_prices = model.predict(future_hours.reshape(-1, 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], name='Actual'))
    fig.add_trace(go.Scatter(x=future_timestamps, y=future_prices, name='Predicted (Next 3 Days)', line=dict(dash='dash')))
    fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)")
    return fig

def get_indicators(df):
    ema = df['price'].ewm(span=20, adjust=False).mean()
    sma = df['price'].rolling(window=20).mean()
    return ema, sma

def get_yoy_mom(df):
    now = df['timestamp'].iloc[-1]
    price_now = df['price'].iloc[-1]
    last_year = now - pd.DateOffset(years=1)
    year_df = df[df['timestamp'] <= last_year]
    price_year = year_df['price'].iloc[-1] if not year_df.empty else price_now
    yoy = ((price_now - price_year) / price_year) * 100 if price_year != 0 else 0
    last_month = now - pd.DateOffset(months=1)
    month_df = df[df['timestamp'] <= last_month]
    price_month = month_df['price'].iloc[-1] if not month_df.empty else price_now
    mom = ((price_now - price_month) / price_month) * 100 if price_month != 0 else 0
    return yoy, mom