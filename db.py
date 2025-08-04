import sqlite3
from sqlite3 import Error
from datetime import datetime

# Function to create a connection to the SQLite database
def create_connection():
    try:
        conn = sqlite3.connect('crypto_dashboard.db')  # SQLite DB file (auto-created)
        print("Connected to SQLite database")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create the table for storing crypto prices
def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

# Function to insert price data into the table
def insert_price(coin, price):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO prices (coin, price)
        VALUES (?, ?)
        ''', (coin, price))
        conn.commit()
        conn.close()

# Function to retrieve prices from the database
def get_prices(coin):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT timestamp, price FROM prices
        WHERE coin = ?
        ORDER BY timestamp ASC
        ''', (coin,))
        rows = cursor.fetchall()
        conn.close()

        prices = []
        for row in rows:
            timestamp = row[0]  # timestamp is already in datetime format
            price = row[1]
            prices.append({'timestamp': timestamp, 'price': price})
        return prices
    return []

# Initialize the database and create the table (call this once)
create_table()
