# filename: stock_analysis.py
# Before running this code, make sure you have the following libraries installed:
# pip install yfinance beautifulsoup4 requests statsmodels prophet scikit-learn tensorflow

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

# Function to retrieve news headlines from Google News
def get_news_headlines(stock_name, num_headlines=10):
    search_url = f"https://news.google.com/search?q={stock_name}&hl=en-IN&gl=IN&ceid=IN%3Aen"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = []
        for i, article in enumerate(soup.find_all('article')):
            if i >= num_headlines:
                break
            try:
                title_element = article.find('h3')
                if title_element:
                  headline = title_element.text.strip()
                  headlines.append(headline)
            except Exception as e:
              print(f"Error extracting headline: {e}")
              continue
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Stock data and financial data from the provided JSON
stock_data = {
  "Tata Steel": {
    "full_name": "Tata Steel",
    "ticker": "TATASTEEL.NS",
    "6_month_percentage_change": 1.52,
    "financial_data": {
      "P/E": 69.666664,
      "Forward P/E": 10.89155,
      "Dividend Yield": 2.37,
      "Price to Book": 2.1341834,
      "Debt/Eq": 109.814,
      "ROE": None
    }
  },
  "Indian Railway Finance Corporation": {
    "full_name": "Indian Railway Finance Corporation",
    "ticker": "IRFC.NS",
    "6_month_percentage_change": -23.08,
    "financial_data": {
      "P/E": 24.311377,
      "Forward P/E": 23.882355,
      "Dividend Yield": 1.35,
      "Price to Book": 3.0528612,
      "Debt/Eq": 785.44,
      "ROE": 0.13036
    }
  },
  "Bharat Petroleum": {
    "full_name": "Bharat Petroleum",
    "ticker": "BPCL.NS",
    "6_month_percentage_change": -17.83,
    "financial_data": {
      "P/E": 8.154899,
      "Forward P/E": 8.457419,
      "Dividend Yield": 5.93,
      "Price to Book": 1.4518532,
      "Debt/Eq": 76.361,
      "ROE": None
    }
  }
}

# Retrieve news headlines for each stock
news_headlines = {}
for stock_name, data in stock_data.items():
    news_headlines[stock_name] = get_news_headlines(data["full_name"])
    print(f"News Headlines for {stock_name}:")
    for headline in news_headlines[stock_name]:
        print(f"- {headline}")
    print("-" * 40)

# Function to fetch stock data from Yahoo Finance
def get_stock_data(ticker, period="5y"):
    data = yf.download(ticker, period=period)
    return data

# Function for MA prediction
def ma_prediction(data, window=50, forecast_days=30):
    data['MA'] = data['Close'].rolling(window=window).mean()
    last_ma = data['MA'].iloc[-1]
    predictions = [last_ma] * forecast_days
    return predictions

# Function for AR prediction
def ar_prediction(data, order=5, forecast_days=30):
    try:
        from statsmodels.tsa.ar.ar_model import AR
        model = AR(data['Close'].dropna())
        model_fit = model.fit()
        predictions = model_fit.predict(start=len(data), end=len(data) + forecast_days-1)
        return predictions
    except ModuleNotFoundError:
        print("AR model not available.  Install statsmodels to use.")
        return None

# Function for ARIMA prediction
def arima_prediction(data, order=(5, 1, 0), forecast_days=30):
    try:
        from statsmodels.tsa.arima.model import ARIMA
        model = ARIMA(data['Close'], order=order)
        model_fit = model.fit()
        predictions = model_fit.predict(start=len(data), end=len(data) + forecast_days-1)
        return predictions
    except ModuleNotFoundError:
        print("ARIMA model not available.  Install statsmodels to use.")
        return None

# Function for SARIMAX prediction
def sarimax_prediction(data, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12), forecast_days=30):
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        model = SARIMAX(data['Close'], order=order, seasonal_order=seasonal_order)
        model_fit = model.fit(disp=False)
        predictions = model_fit.predict(start=len(data), end=len(data) + forecast_days-1)
        return predictions
    except ModuleNotFoundError:
        print("SARIMAX model not available. Install statsmodels to use.")
        return None

# Function for LSTM prediction
def lstm_prediction(data, forecast_days=30):
    try:
        from sklearn.preprocessing import MinMaxScaler
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense

        # Scale the data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Prepare data for LSTM
        def prepare_data(data, n_steps):
            X, y = [], []
            for i in range(len(data) - n_steps):
                X.append(data[i:(i + n_steps)])
                y.append(data[i + n_steps])
            return np.array(X), np.array(y)

        n_steps = 50  # Number of time steps
        X, y = prepare_data(scaled_data, n_steps)
        X = X.reshape(X.shape[0], X.shape[1], 1)

        # Build LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(n_steps, 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X, y, epochs=10, batch_size=32, verbose=0)

        # Make predictions
        last_n_days = scaled_data[-n_steps:]
        predictions = []
        for _ in range(forecast_days):
            x_input = last_n_days.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            predictions.append(yhat[0, 0])
            last_n_days = np.append(last_n_days[1:], yhat)
            last_n_days = last_n_days.reshape(-1, 1)

        # Inverse transform the predictions
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()

    except ModuleNotFoundError:
        print("Tensorflow and/or scikit-learn not available. Install to use LSTM.")
        return None

# Function for Prophet prediction
def prophet_prediction(data, forecast_days=30):
    try:
        from prophet import Prophet
        df = data.reset_index()[['Date', 'Close']]
        df.columns = ['ds', 'y']
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        predictions = forecast['yhat'].tail(forecast_days).values
        return predictions
    except ModuleNotFoundError:
        print("Prophet model not available. Install prophet to use.")
        return None

# Technical Analysis Indicators
def calculate_rsi(data, period=14):
    if len(data) == 0:
        return np.nan
    delta = data['Close'].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(period).mean()
    roll_down = down.abs().rolling(period).mean()
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    if len(data) == 0:
        return np.nan, np.nan

    EMA_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    EMA_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
    MACD = EMA_fast - EMA_slow
    Signal = MACD.ewm(span=signal_period, adjust=False).mean()
    return MACD, Signal

# Prediction function combining all methods
def predict_stock_price(ticker, financial_data, news_headlines, forecast_days=30):
    data = get_stock_data(ticker)
    if data.empty:
        print(f"Could not retrieve data for {ticker}")
        return None

    # Calculate Technical Indicators
    rsi = calculate_rsi(data)
    macd, signal = calculate_macd(data)

    # Extract last values, handling potential NaNs
    rsi_value = float(rsi.iloc[-1]) if isinstance(rsi, pd.Series) and not pd.isna(rsi.iloc[-1]) else np.nan
    macd_value = float(macd.iloc[-1]) if isinstance(macd, pd.Series) and not pd.isna(macd.iloc[-1]) else np.nan
    signal_value = float(signal.iloc[-1]) if isinstance(signal, pd.Series) and not pd.isna(signal.iloc[-1]) else np.nan


    # MA Prediction
    ma_preds = ma_prediction(data.copy(), forecast_days=forecast_days)
    # AR Prediction
    ar_preds = ar_prediction(data.copy(), forecast_days=forecast_days)
    # ARIMA Prediction
    arima_preds = arima_prediction(data.copy(), forecast_days=forecast_days)
    # SARIMAX Prediction
    sarimax_preds = sarimax_prediction(data.copy(), forecast_days=forecast_days)
    # LSTM Prediction
    lstm_preds = lstm_prediction(data.copy(), forecast_days=forecast_days)
    # Prophet Prediction
    prophet_preds = prophet_prediction(data.copy(), forecast_days=forecast_days)

    predictions = [ma_preds]
    if ar_preds is not None:
        predictions.append(ar_preds)
    if arima_preds is not None:
        predictions.append(arima_preds)
    if sarimax_preds is not None:
        predictions.append(sarimax_preds)
    if prophet_preds is not None:
        predictions.append(prophet_preds)
    if lstm_preds is not None:
        predictions.append(lstm_preds)

    # Combine predictions (you can adjust weights based on backtesting)
    combined_preds = np.mean([pred for pred in predictions if pred is not None], axis=0)

    # Incorporate Fundamental Analysis (example: adjust based on P/E ratio)
    pe_ratio = financial_data['P/E']
    if pe_ratio is not None:
        if pe_ratio > 30:  # Overvalued, reduce prediction
            combined_preds *= 0.95
        elif pe_ratio < 15:  # Undervalued, increase prediction
            combined_preds *= 1.05

    # Incorporate News Sentiment (Placeholder - requires sentiment analysis)
    # In a real scenario, you would analyze the news headlines and adjust the predictions accordingly.
    # For example, if there's overwhelmingly negative news, you might reduce the prediction.

    # Example of stop-loss (e.g., 5% below the last closing price)
    last_close = float(data['Close'].iloc[-1]) if len(data['Close']) > 0 else 0
    stop_loss = last_close * 0.95

    # Create a DataFrame for the predictions
    future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, forecast_days + 1)]
    predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': combined_preds})
    predictions_df = predictions_df.set_index('Date')

    return predictions_df, stop_loss, rsi_value, macd_value, signal_value

# Analyze and predict for each stock
all_predictions = {}
for stock_name, data in stock_data.items():
    print(f"Analyzing {stock_name}...")
    predictions, stop_loss, rsi, macd, signal = predict_stock_price(data["ticker"], data["financial_data"], news_headlines[stock_name])
    if predictions is not None:
        all_predictions[stock_name] = {
            "predictions": predictions,
            "stop_loss": stop_loss,
            "rsi": rsi,
            "macd": macd,
            "signal": signal
        }

        print(f"  Predictions for {stock_name}:")
        print(predictions)
        print(f"  Suggested Stop-Loss: {stop_loss:.2f}")
        print(f"  Latest RSI: {rsi:.2f}")
        print(f"  Latest MACD: {macd:.2f}, Signal Line: {signal:.2f}")
    print("-" * 40)

# Plotting the predictions
for stock_name, results in all_predictions.items():
    plt.figure(figsize=(12, 6))
    plt.plot(results["predictions"]['Predicted_Close'], label='Predicted Close Price')
    plt.title(f'Stock Price Prediction for {stock_name}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{stock_name}_prediction.png')  # Save the plot
    plt.close() # Close the plot to free memory

print("Predictions generated and saved to files.")