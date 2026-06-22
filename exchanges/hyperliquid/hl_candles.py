
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

# create & normalize hyperliquid candles dataframe
def build_hl_candles_df(token_name_hl, start_time_stamp, end_time_stamp, interval):

    hl_candles_df = pd.DataFrame(get_hl_candles(token_name_hl, start_time_stamp, end_time_stamp, interval) ) # convert to dataframe

    for col in ["t", "T"]:
        hl_candles_df[col] = pd.to_datetime(hl_candles_df[col], unit="ms", utc=True) # convert unix to date-time format
        hl_candles_df[col] = hl_candles_df[col].dt.tz_localize(None) # remove UTC time zone

    for col in ["o", "c", "h", "l", "v"]:
        hl_candles_df[col] = pd.to_numeric(hl_candles_df[col]) # convert strings to numeric format

    # compute typical price and notional volume
    hl_candles_df["typical_px"] = (hl_candles_df["h"] + hl_candles_df["l"] + hl_candles_df["c"]) / 3
    hl_candles_df["ntl_vlm"] = hl_candles_df["typical_px"] * hl_candles_df["v"]

    return hl_candles_df
