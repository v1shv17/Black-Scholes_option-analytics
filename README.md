# Black-Scholes Options Pricing & Data ETL Pipeline

## Description
This project implements an **options analytics tool** based on the **Black-Scholes model**, integrating real-time options data from **Yahoo Finance** and storing it in a **PostgreSQL database**. The tool automates data fetching, processing, and storage, making it useful for **quantitative finance**, **derivatives trading**, and **risk analysis**. Key features include:

- **Real-time data extraction** using `yfinance`
- **Options pricing calculation** via the Black-Scholes formula
- **Automated ETL pipeline** to store structured data in PostgreSQL
- **Support for multiple stock symbols and option chains**

## Installation

Ensure you have **Python 3.8+** and the required dependencies installed:

```sh
pip install numpy scipy yfinance pandas psycopg2
```

### Database Setup
1. Ensure **PostgreSQL** is installed and running.
2. Update the database connection details in the script:
   ```python
   DB_NAME = "black_scholes_db"
   DB_USER = "black_scholes_user"
   DB_PASSWORD = "your_password"
   DB_HOST = "localhost"
   DB_PORT = "5432"
   ```
3. Run the script to **create the database schema**:
   ```sh
   python your_script.py
   ```

## Usage
Run the ETL pipeline for a specific stock symbol (e.g., Apple - AAPL):

```sh
python your_script.py
```

Or modify the script to accept user input:

```python
if __name__ == "__main__":
    symbol = input("Enter stock symbol: ")
    etl_pipeline(symbol)
```

### Example Calculation (Black-Scholes Model)
```python
from your_script import black_scholes

call_price = black_scholes(S=150, K=145, T=0.5, r=0.03, sigma=0.25, option_type="call")
print(f"Call Option Price: {call_price}")
```

## Output Example
After running the script, you will see output like this:
```sh
Fetching options data for AAPL...
Data successfully inserted for AAPL
```
For a specific Black-Scholes calculation:
```sh
Call Option Price: 12.34
```
## Database Table Output

Here is an example of the `options_data` table populated with retrieved options contracts:
![Screenshot](Screenshot%202025-02-14%20at%204.36.49%20PM%205.07.20%20PM.png)

## How is This Useful?
- **Traders & Analysts**: Evaluate option prices and potential market moves.
- **Researchers**: Study historical options pricing trends.
- **Developers**: Extend the tool to support additional financial models.

## What Can You Do With It?
- Backtest trading strategies with historical data.
- Integrate with other financial tools for enhanced analysis.
- Build a real-time options analytics dashboard.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit changes and submit a pull request

Ensure adherence to Python best practices and PEP-8 styling.

## Contact
For any questions or suggestions, open an issue or reach out via GitHub.

