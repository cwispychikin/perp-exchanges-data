import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../coinglass_api_key.env")
coinglass_api_key = os.getenv("COINGLASS_API_KEY")

if coinglass_api_key is None:
    raise ValueError("COINGLASS_API_KEY not loaded")

def binance_oi(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    url = "https://open-api-v4.coinglass.com/api/futures/open-interest/history"
    headers = {
        "accept": "application/json",
        "CG-API-KEY": coinglass_api_key
    }
    params = {
        "exchange": "Binance",
        "symbol": cg_token_name_binance,
        "interval": interval,
        "start_time": start_time_stamp,
        "end_time": end_time_stamp
    }

    response = requests.get(url, headers = headers, params = params)
    binance_oi = response.json()

    binance_oi_df = pd.DataFrame(binance_oi["data"])

    binance_oi_df["time"] = pd.to_datetime(binance_oi_df["time"], unit = "ms") # convert unix to date-time

    for col in ["open", "high", "low", "close"]:
        binance_oi_df[col] = pd.to_numeric(binance_oi_df[col]) # convert strings to numeric format

    return binance_oi_df