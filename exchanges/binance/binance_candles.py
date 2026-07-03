
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

# create dataframe, format data
def build_binance_candles_df(token_name_binance, interval, start_time_stamp, end_time_stamp, limit):

    binance_candles_df = pd.DataFrame(get_binance_candles(token_name_binance, interval, start_time_stamp, end_time_stamp, limit)) # convert to dataframe

    binance_candles_df.columns = [
        "start_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "end_time",
        "notional_volume",
        "trade_count",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore"
    ]

    for col in ["start_time", "end_time"]:
        binance_candles_df[col] = pd.to_datetime(binance_candles_df[col], unit = "ms") # convert unix to date-time format

    for col in ["open", "high", "low", "close", "notional_volume", "volume", "trade_count", "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"]:
        binance_candles_df[col] = pd.to_numeric(binance_candles_df[col]) # convert strings to numeric format

    return binance_candles_df
