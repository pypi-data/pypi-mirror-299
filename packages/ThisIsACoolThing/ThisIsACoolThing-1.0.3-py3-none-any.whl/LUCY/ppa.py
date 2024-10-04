import os
from pathlib import Path
import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import pkg_resources

base_dir = Path(__file__).resolve().parent
model_path = base_dir / 'eth_lstm_best_model_1hour.h5'
scaler_path = pkg_resources.resource_filename(__name__, 'scaler_custom.pkl')

model = tf.keras.models.load_model(model_path)
scaler = joblib.load(scaler_path)

binance = ccxt.binance()

def fetch_current_price(symbol):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

def fetch_latest_close_data(symbol, timeframe='1h', limit=120):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        close_prices = np.array([x[4] for x in ohlcv])
        return close_prices
    except Exception as e:
        print(f"Error fetching latest close data: {str(e)}")
        return None

def fetch_ohlcv(symbol, timeframe='1h', limit=500):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {str(e)}")
        return None

def inverse_min_max_scale(scaled_data, data_min, data_max, feature_range=(0, 1)):
    scale = (data_max - data_min) / (feature_range[1] - feature_range[0])
    return scaled_data * scale + data_min

def min_max_scale(data, data_min, data_max, feature_range=(0, 1)):
    scale = (feature_range[1] - feature_range[0]) / (data_max - data_min)
    min_range = feature_range[0]
    return scale * (data - data_min) + min_range

scaler_data = joblib.load(scaler_path)
data_min = scaler_data['min']
data_max = scaler_data['max']

def predict_one_hour():
    symbol = 'ETH/USDT'

    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return

    latest_close_data = fetch_latest_close_data(symbol=symbol, timeframe='1h', limit=120)
    
    if latest_close_data is None or len(latest_close_data) < 120:
        print('Not enough data to make a prediction. Exiting.')
        return

    latest_close_data_scaled = min_max_scale(latest_close_data.reshape(-1, 1), data_min, data_max)
    latest_close_data_scaled = latest_close_data_scaled.reshape(1, latest_close_data_scaled.shape[0], 1)

    predicted_price_scaled = model.predict(latest_close_data_scaled, verbose=0)
    predicted_price = inverse_min_max_scale(predicted_price_scaled[0], data_min, data_max)[0]

    percentage_change = ((predicted_price - current_price) / current_price) * 100

    ohlcv_df = fetch_ohlcv(symbol, timeframe='1h', limit=500)
    if ohlcv_df is None:
        print("Unable to fetch OHLCV data. Exiting.")
        return

    print(f"\033[90mOutput:\033[0m Predicted price (1h): ${round(predicted_price, 2)}")
    print(f"        Price: ${round(current_price, 2)}")
    print(f"        Percentage: {round(percentage_change, 2)}%")

    suggestion = generate_suggestion(percentage_change)
    print(f"        Market Suggestion: {suggestion}")

def generate_suggestion(percentage_change):
    if percentage_change > 0.5:
        return "\033[92mSuggested Buy\033[0m"
    elif percentage_change < -0.5:
        return "\033[91mSuggested Sell\033[0m"
    elif 0.2 <= percentage_change <= 0.5:
        return "\033[92mShort Buy\033[0m"
    elif -0.5 <= percentage_change <= -0.2:
        return "\033[91mShort Sell\033[0m"
    else:
        return "\033[90mNEUTRAL\033[0m"
    
def print_lucy_rainbow():

    red = '\033[91m'
    orange = '\033[93m'
    green = '\033[92m'
    blue = '\033[94m'
    reset = '\033[0m'

    print(f"{red}L {orange}U {green}C {blue}Y {reset}")

def main():

    print("Welcome to") 
    print_lucy_rainbow()
    
    while True:
        user_input = input("\n\033[90mInput:\033[0m  ")

        if user_input == "pr":
            predict_one_hour()
        elif user_input == "exit":
            print(f"\033[90mOutput:\033[0m Exiting...")
            break
        else:
            print("\033[90mOutput:\033[0m Invalid command, try again")

if __name__ == '__main__':
    main() 
