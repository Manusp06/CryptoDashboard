import streamlit as st
import pandas as pd
import sqlite3
import requests
from analytics import (
    get_candlestick_data,
    get_prediction_chart,
    get_future_prediction_chart,
    get_indicators,
    get_yoy_mom
)

DB_PATH = "crypto_data.db"

COINS = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]

def fetch_current_price(coin):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin, "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()[coin]["usd"]
    return None

def get_historical_df(coin):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT timestamp, price FROM prices WHERE coin='{coin}' ORDER BY timestamp ASC", conn
    )
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Sidebar: Only dropdown for coin selection
st.sidebar.title("Select Cryptocurrency")
# coin = st.sidebar.selectbox("Choose coin", ["bitcoin", "ethereum"])
coin = st.sidebar.selectbox("Choose coin", COINS)
st.sidebar.caption("Timezone is UTC. Refresh page every 15 min for latest prices.")

st.title("🚀 Crypto Dashboard")
st.header(f"{coin.capitalize()} Analysis")

# Fetch data for selected coin
df = get_historical_df(coin)
current_price = fetch_current_price(coin)

# Price & Volume Metrics
last_24h = df[df['timestamp'] >= (df['timestamp'].max() - pd.Timedelta(hours=24))]
volume_24h = last_24h['price'].count()  # Replace with actual volume column if available
high_24h = last_24h['price'].max() if not last_24h.empty else df['price'].max()
low_24h = last_24h['price'].min() if not last_24h.empty else df['price'].min()
daily_range = high_24h - low_24h
price_24h_ago = last_24h['price'].iloc[0] if len(last_24h) > 0 else df['price'].iloc[0]

if current_price is not None and price_24h_ago is not None and price_24h_ago != 0:
    change_24h = ((current_price - price_24h_ago) / price_24h_ago * 100)
else:
    change_24h = None

with st.expander("💹 Price & Volume Metrics", expanded=True):
    st.write(f"**Current Price:** ${current_price:,.2f}" if current_price is not None else "N/A")
    st.write(f"**Volume (24h):** {volume_24h:,}")
    st.write(f"**Daily Range (24h):** ${daily_range:,.2f}")
    st.write(f"**24h Change:** {change_24h:.2f}%" if change_24h is not None else "N/A")

with st.expander("📊 Candlestick Chart", expanded=True):
    fig = get_candlestick_data(df)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("🔮 Price Prediction (LSTM - Demo)", expanded=False):
    pred_fig = get_prediction_chart(df)
    st.plotly_chart(pred_fig, use_container_width=True)

with st.expander("📈 Future Price Prediction (Next 3 Days)", expanded=True):
    future_fig = get_future_prediction_chart(df, days_ahead=3)
    st.plotly_chart(future_fig, use_container_width=True)

with st.expander("📈 Technical Indicators", expanded=False):
    ema, sma = get_indicators(df)
    st.write(f"**EMA (20):** {ema.iloc[-1]:.2f}")
    st.write(f"**SMA (20):** {sma.iloc[-1]:.2f}")

with st.expander("📋 Key Metrics", expanded=False):
    st.write(f"**High:** {df['price'].max():.2f}")
    st.write(f"**Low:** {df['price'].min():.2f}")
    st.write(f"**Open:** {df['price'].iloc[0]:.2f}")
    st.write(f"**Close:** {df['price'].iloc[-1]:.2f}")

with st.expander("📅 Year-over-Year & Month-over-Month Change", expanded=False):
    yoy, mom = get_yoy_mom(df)
    st.write(f"**YoY Change:** {yoy:.2f}%")
    st.write(f"**MoM Change:** {mom:.2f}%")