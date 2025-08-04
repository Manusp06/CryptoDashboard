**Crypto Dashboard and ETL Pipeline**
This repository contains a Crypto Dashboard built using Streamlit that fetches real-time and historical data for various cryptocurrencies. Additionally, an ETL pipeline is included that continuously fetches and stores cryptocurrency data in a SQLite database.

The project utilizes the CoinGecko API to retrieve cryptocurrency data and includes features like price tracking, price prediction (using LSTM), technical analysis indicators, and more.

**📦 Contents**
app.py: Main Streamlit application that visualizes cryptocurrency data.

analytics.py: Contains functions for performing technical analysis and generating visualizations like candlestick charts, price predictions, and technical indicators.

etl_pipeline.py: Script for fetching and storing historical and real-time cryptocurrency price data in a SQLite database.

crypto_data.db: SQLite database to store cryptocurrency price data (not included, generated during ETL pipeline execution).

**🔧 Setup Instructions**
Prerequisites
To run this project, ensure you have the following installed:

Python 3.7 or higher

Streamlit

Pandas

Plotly

Scikit-learn

SQLite3 (comes with Python by default)

**Installation**
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/crypto-dashboard.git
cd crypto-dashboard
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt file, you can manually install dependencies:

bash
Copy
Edit
pip install streamlit pandas plotly scikit-learn requests
⚙️ How to Use
1. Running the Streamlit Dashboard
To start the Streamlit application, run the following command:

bash
Copy
Edit
streamlit run app.py
This will open the application in your default web browser.

**2. Features in the Dashboard**
Cryptocurrency Selection: Choose from a list of available cryptocurrencies (Bitcoin, Ethereum, Solana, Cardano, Dogecoin) using a dropdown in the sidebar.

Price & Volume Metrics: Displays the current price, 24-hour volume (based on available data), daily range, and price change over the last 24 hours.

Candlestick Chart: Visualizes a candlestick chart showing the price movements of the selected cryptocurrency.

Price Prediction (LSTM Demo): Displays a simple moving average as a predicted price for the cryptocurrency.

Future Price Prediction: Predicts the future price of the selected coin for the next 3 days using linear regression.

Technical Indicators: Shows the 20-period Exponential Moving Average (EMA) and Simple Moving Average (SMA).

Year-over-Year (YoY) & Month-over-Month (MoM) Change: Displays the percentage change in price compared to the same day last year and the previous month.

**3. Running the ETL Pipeline**
To fetch and store historical data for all coins, you can run the ETL pipeline script. This will store the data in an SQLite database.

Run the ETL pipeline:

bash
Copy
Edit
python etl_pipeline.py
This script will fetch data for the past 3 days for each cryptocurrency and store it in the database.

To continuously update the database with real-time price data every 15 minutes, uncomment the run_price_updater() function in etl_pipeline.py:

python
Copy
Edit
This will fetch and store the current price of each coin every 15 minutes.

**📚 How It Works**
app.py (Streamlit Dashboard)
Fetches historical cryptocurrency data from a SQLite database.

Displays the latest price along with the 24-hour change, high/low range, and volume (if available).

Generates visualizations such as candlestick charts and price predictions.

Uses the analytics.py functions to handle calculations and visualizations.

analytics.py (Technical Analysis)
get_candlestick_data(df): Generates a candlestick chart using historical data.

get_prediction_chart(df): Provides a predicted price line using the moving average.

get_future_prediction_chart(df, days_ahead): Predicts the next 3 days' prices using a linear regression model.

get_indicators(df): Calculates the 20-period Exponential Moving Average (EMA) and Simple Moving Average (SMA).

get_yoy_mom(df): Calculates the Year-over-Year (YoY) and Month-over-Month (MoM) percentage changes.

etl_pipeline.py (ETL Pipeline)
Fetches cryptocurrency data from the CoinGecko API.

Stores the data in a SQLite database (crypto_data.db).

The script fetches both historical data (past 3 days) and real-time prices.

The real-time price fetching can be set to run continuously every 15 minutes.

**🛠️ Customization**
Adding New Coins: You can modify the COINS list in both app.py and etl_pipeline.py to add more cryptocurrencies.

API Settings: The CoinGecko API can be adjusted for more advanced features like fetching historical data for longer periods. Refer to the CoinGecko API Documentation for more details.

Price Prediction Models: The LSTM model used in get_prediction_chart can be replaced with more advanced models or extended to provide more accurate predictions.

Database Storage: The SQLite database is used for storage. You can switch to a more robust database like PostgreSQL or MySQL if needed by modifying the store_prices_in_db function in etl_pipeline.py.

**🚧 Limitations**
Data Gaps: The price data fetched from the CoinGecko API may have gaps or missing values, especially for less popular coins.

Real-Time Limitations: The CoinGecko API rate limits requests, and the real-time price fetching process is limited to one request every 15 minutes to avoid hitting the API rate limits.

Prediction Model: The current prediction model is based on a simple moving average and linear regression, which are basic techniques. For more accurate predictions, more complex models (e.g., LSTM or ARIMA) could be incorporated
