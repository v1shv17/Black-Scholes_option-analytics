import numpy as np
from scipy.stats import norm
import yfinance as yf
import pandas as pd
import psycopg2
from psycopg2 import sql

# Database Connection Details (Update these)
DB_NAME = "black_scholes_db"
DB_USER = "black_scholes_user"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Step 1: Connect to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        exit()

# Step 2: Create Table Schema (Ensure correct permissions)
def create_database_schema():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS options_data (
        id SERIAL PRIMARY KEY,
        stock_symbol VARCHAR(10) NOT NULL,
        strike_price FLOAT NOT NULL,
        current_price FLOAT NOT NULL,
        time_to_maturity FLOAT NOT NULL,
        risk_free_rate FLOAT NOT NULL,
        volatility FLOAT NOT NULL,
        call_price FLOAT NOT NULL,
        put_price FLOAT NOT NULL,
        expiration_date DATE NOT NULL
    );
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# Step 3: Black-Scholes Model
def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

# Step 4: Fetch Data from Yahoo Finance API
import yfinance as yf

# Step 4: Fetch Data from Yahoo Finance using yfinance
def fetch_options_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        options_dates = stock.options  # List of expiration dates
        all_options = []

        for expiration_date in options_dates:
            options = stock.option_chain(expiration_date)
            calls = options.calls
            puts = options.puts

            # Add expiration date to each option
            calls['expiration'] = expiration_date
            puts['expiration'] = expiration_date

            # Combine calls and puts
            all_options.append((calls, puts))

        return all_options
    except Exception as e:
        raise Exception(f"Failed to fetch options data for {symbol}: {e}")

def etl_pipeline(symbol):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Ensure table exists
    create_database_schema()

    # Fetch options data
    try:
        options_data = fetch_options_data(symbol)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    for calls, puts in options_data:
        for _, option in pd.concat([calls, puts]).iterrows():
            S = option.get('lastPrice', 0)
            K = option.get('strike', 0)
            expiration_date = pd.to_datetime(option.get('expiration')).date()

            # Calculate time to maturity
            T = (pd.to_datetime(expiration_date) - pd.Timestamp.now()).days / 365

            r = 0.03  # Fixed risk-free rate for now

            # Handle missing volatility data
            sigma = option.get('impliedVolatility', None)
            if sigma is None or sigma == 0:
                print(f"Skipping option {symbol} with strike {K} due to missing volatility.")
                continue

            # Calculate call and put prices using Black-Scholes
            option_type = 'call' if option.get('contractSymbol', '').endswith('C') else 'put'
            price = black_scholes(S, K, T, r, sigma, option_type)

            # Insert data into PostgreSQL
            try:
                cursor.execute(
                    sql.SQL("""
                    INSERT INTO options_data (stock_symbol, strike_price, current_price, time_to_maturity, 
                                              risk_free_rate, volatility, call_price, put_price, expiration_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """),
                    (symbol, K, S, T, r, sigma, price if option_type == 'call' else None,
                     price if option_type == 'put' else None, expiration_date)
                )
            except Exception as e:
                print(f"Error inserting data: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data successfully inserted for {symbol}")


# Main Execution
if __name__ == "__main__":
    symbol = "AAPL"  # Example: Apple Stock
    etl_pipeline(symbol)
