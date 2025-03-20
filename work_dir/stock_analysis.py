# filename: stock_analysis.py
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the stocks
stocks = ['RELIANCE.NS', 'TATAMOTORS.NS']  # NSE tickers
stock_names = ['Reliance', 'Tata Motors']
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(months=6)

# Fetch historical data using yfinance
data = yf.download(stocks, start=start_date, end=end_date)

# Access 'Adj Close' data using MultiIndex
adj_close = data[[('Close', stock) for stock in stocks]]

# Rename columns
adj_close.columns = stock_names

# Calculate percentage change over 6 months
start_prices = adj_close.iloc[0]
end_prices = adj_close.iloc[-1]
percentage_change = ((end_prices - start_prices) / start_prices) * 100

print("Percentage Change Over 6 Months:")
print(percentage_change)

# Fetch financial metrics (using yfinance's Ticker object)
financial_data = {}
for ticker, name in zip(stocks, stock_names):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        financial_data[name] = {
            'P/E Ratio': info.get('trailingPE'),
            'Forward P/E': info.get('forwardPE'),
            'Dividends': info.get('dividendRate'),
            'Price to Book': info.get('priceToBook'),
            'Debt/Eq': info.get('debtToEquity'),
            'ROE': info.get('returnOnEquity')
        }
    except Exception as e:
        print(f"Could not fetch financial data for {name}: {e}")
        financial_data[name] = {} #Store as empty if cannot retrieve.

print("\nFinancial Metrics:")
print(pd.DataFrame(financial_data))


# Normalize the stock prices
normalized_data = adj_close / adj_close.iloc[0]

# Check for NaN values
if normalized_data.isnull().values.all():
    print("\nWARNING: The normalized data contains only NaN values.")
else:
    print("\nNormalized data does not contain all NaN values.")

# Calculate correlation
returns = adj_close.pct_change().dropna()
correlation_matrix = returns.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

#Visualization
plt.figure(figsize=(12, 6))
for stock in stock_names:
    plt.plot(normalized_data.index, normalized_data[stock], label=stock)

plt.title('Normalized Stock Prices')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend()
plt.grid(True)
plt.savefig('normalized_prices.png')
plt.show()