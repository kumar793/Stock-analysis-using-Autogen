# filename: stock_analysis.py
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the tickers
tickers = ['DLF.NS', 'BAJFINANCE.NS']
stock_names = ['DLF', 'BAJAJ FINSERV'] # Added descriptive names

# Set the time period for historical data
period = '6mo'

# Download historical data
data = yf.download(tickers, period=period)

# Extract adjusted close prices
adj_close = data['Adj Close']

# Calculate percentage change over 6 months
start_prices = adj_close.iloc[0]
end_prices = adj_close.iloc[-1]
performance = ((end_prices - start_prices) / start_prices) * 100

print("Stock Performance over the Past 6 Months:")
for i, ticker in enumerate(tickers):
    print(f"{stock_names[i]}: {performance[ticker]:.2f}%")

# Normalize the stock prices
normalized_prices = adj_close / adj_close.iloc[0]

# Plot the normalized prices
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(normalized_prices[ticker], label=stock_names[tickers.index(ticker)]) # Using descriptive names

plt.title('Normalized Stock Prices')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend()
plt.grid(True)
plt.savefig('normalized_prices.png')
plt.show()

# Analyze correlation
correlation_matrix = adj_close.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Get financial data
for i, ticker in enumerate(tickers):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print(f"\nFinancial Data for {stock_names[i]}:") # Using descriptive names
        print(f"  P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"  Forward P/E: {info.get('forwardPE', 'N/A')}")
        print(f"  Dividend Yield: {info.get('dividendYield', 'N/A')}")
        print(f"  Price to Book: {info.get('priceToBook', 'N/A')}")
        print(f"  Debt/Equity: {info.get('debtToEquity', 'N/A')}")
        print(f"  Return on Equity: {info.get('returnOnEquity', 'N/A')}")

    except Exception as e:
        print(f"Error retrieving financial data for {stock_names[i]}: {e}") # Using descriptive names