
import requests
import pandas as pd

# get historical price and volume
def get_hl_candles(token_name_hl, start_time_stamp, end_time_stamp, interval):

    # API call
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": token_name_hl, # can prefix with DEX name (e.g., xyz:XYZ100)
            "interval": interval,
            "startTime": start_time_stamp,
            "endTime": end_time_stamp
        }
    }

    response = requests.post(url, json = payload)
    hl_candles = response.json()

    return hl_candles

# create dataframe, format data
def build_hl_candles_df(token_name_hl, start_time_stamp, end_time_stamp, interval):

    hl_candles_df = pd.DataFrame(get_hl_candles(token_name_hl, start_time_stamp, end_time_stamp, interval) ) # convert to dataframe

    hl_candles_df = hl_candles_df.rename(columns = {
        "T": "end_time",
        "t": "start_time",
        "s": "token",
        "i": "interval",
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume",
        "n": "trade_count"
    })

    for col in ["start_time", "end_time"]:
        hl_candles_df[col] = pd.to_datetime(hl_candles_df[col], unit = "ms") # convert unix to date-time format

    for col in ["open", "close", "high", "low", "volume"]:
        hl_candles_df[col] = pd.to_numeric(hl_candles_df[col]) # convert strings to numeric format

    # compute typical price and notional volume
    hl_candles_df["typical_price"] = (hl_candles_df["high"] + hl_candles_df["low"] + hl_candles_df["close"]) / 3
    hl_candles_df["notional_volume"] = hl_candles_df["typical_price"] * hl_candles_df["volume"]

    return hl_candles_df
