import yfinance as yf

# Define the stock ticker symbol
ticker_symbol = "NVDA"  

# Get the stock object
stock = yf.Ticker(ticker_symbol)

# Fetch available expiration dates for options
expirations = stock.options
print(f"Available Expiration Dates: {expirations}")

# Select an expiration date (use the first available one)
if expirations:
    selected_date = expirations[0]
    print(f"Fetching options for expiration date: {selected_date}")

    # Get options chain data for the selected expiration date
    options_chain = stock.option_chain(selected_date)

    # Print Call and Put options
    print("\nCALL OPTIONS:")
    print(options_chain.calls)

    print("\nPUT OPTIONS:")
    print(options_chain.puts)
else:
    print("No options data available for this stock.")
