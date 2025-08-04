import requests
import sqlite3
from datetime import datetime, timedelta
import time

COINS = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]

def fetch_historical_data(coin, days=3):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    params = {
        "vs_currency": "usd",
        "from": start_timestamp,
        "to": end_timestamp
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'prices' in data and data['prices']:
            print(f"Data fetched successfully for {coin}")
            return data['prices']
        else:
            print(f"No price data found for {coin} in the specified date range.")
            return None
    elif response.status_code == 422:
        print(f"HTTP 422 Error: Invalid parameters for {coin}. Please check your request.")
        return None
    else:
        print(f"Error fetching data for {coin}. HTTP Status Code: {response.status_code}")
        return None

def store_prices_in_db(prices, coin):
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT,
            timestamp INTEGER,
            price REAL
        )
    """)
    for entry in prices:
        timestamp_ms, price = entry
        cursor.execute(
            "INSERT INTO prices (coin, timestamp, price) VALUES (?, ?, ?)",
            (coin, timestamp_ms, price)
        )
    conn.commit()
    conn.close()
    print(f"Stored {len(prices)} records for {coin}.")

def fetch_and_store_current_price(coin):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin, "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        price = response.json()[coin]["usd"]
        timestamp_ms = int(datetime.now().timestamp() * 1000)
        store_prices_in_db([[timestamp_ms, price]], coin)
        print(f"Current price for {coin} stored: {price}")
    else:
        print(f"Failed to fetch current price for {coin}")

# Fetch and store historical data for all coins (run once)
for coin in COINS:
    prices = fetch_historical_data(coin, days=3)
    if prices:
        store_prices_in_db(prices, coin)

# Fetch and store current price every 15 minutes
def run_price_updater():
    while True:
        for coin in COINS:
            fetch_and_store_current_price(coin)
        time.sleep(900)  # 15 minutes

# Uncomment the next line to enable continuous updating
# run_price_updater()