
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../coinglass_api_key.env")
coinglass_api_key = os.getenv("COINGLASS_API_KEY")

if coinglass_api_key is None:
    raise ValueError("COINGLASS_API_KEY not loaded")

# get open interest
def get_hl_oi(cg_token_name_hl, interval, start_time_stamp, end_time_stamp):

    # API call
    url = "https://open-api-v4.coinglass.com/api/futures/open-interest/history"
    headers = {
        "accept": "application/json",
        "CG-API-KEY": coinglass_api_key
    }
    params = {
        "exchange": "Hyperliquid",
        "symbol": cg_token_name_hl,
        "interval": interval,
        "start_time": start_time_stamp,
        "end_time": end_time_stamp
    }

    response = requests.get(url, headers = headers, params = params)
    hl_oi = response.json()

    return hl_oi

# create dataframe, format data
def build_hl_oi_df(cg_token_name_hl, interval, start_time_stamp, end_time_stamp):

    hl_oi = get_hl_oi(cg_token_name_hl, interval, start_time_stamp, end_time_stamp)
    hl_oi_df = pd.DataFrame(hl_oi["data"])

    hl_oi_df["time"] = pd.to_datetime(hl_oi_df["time"], unit = "ms") # convert unix to date-time

    for col in ["open", "high", "low", "close"]:
        hl_oi_df[col] = pd.to_numeric(hl_oi_df[col]) # convert strings to numeric format

    return hl_oi_df








