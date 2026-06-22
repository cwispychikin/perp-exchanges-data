
import requests
import pandas as pd

# get candles
def get_binance_candles(token_name_binance, interval, start_time_stamp, end_time_stamp, limit):

    # API call
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": token_name_binance,
        "interval": interval,
        "startTime": start_time_stamp,
        "endTime": end_time_stamp,
        "limit": limit
    }

    response  = requests.get(url, params = params)
    binance_candles = response.json()

    return binance_candles

# create & normalize binance candles dataframe
def build_binance_candles_df(token_name_binance, interval, start_time_stamp, end_time_stamp, limit):

    binance_candles_df = pd.DataFrame(get_binance_candles(token_name_binance, interval, start_time_stamp, end_time_stamp, limit)) # convert to dataframe

    binance_candles_df.columns = [
        "Open Time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close Time",
        "Quote Asset Volume",
        "No. of Trades",
        "Taker Buy Base Asset Volume",
        "Taker Buy Quote Asset Volume",
        "Ignore"
    ]

    for col in ["Open Time", "Close Time"]:
        binance_candles_df[col] = pd.to_datetime(binance_candles_df[col], unit = "ms") # convert unix to date-time format

    for col in ["Open", "High", "Low", "Close", "Volume", "Quote Asset Volume", "No. of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"]:
        binance_candles_df[col] = pd.to_numeric(binance_candles_df[col]) # convert strings to numeric format

    return binance_candles_df
