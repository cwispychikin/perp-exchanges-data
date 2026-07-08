import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../coinglass_api_key.env")
coinglass_api_key = os.getenv("COINGLASS_API_KEY")

if coinglass_api_key is None:
    raise ValueError("COINGLASS_API_KEY not loaded")

def binance_liquidation(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    url = "https://open-api-v4.coinglass.com/api/futures/liquidation/history"
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
    binance_liquidation = response.json()

    binance_liquidation_df = pd.DataFrame(binance_liquidation["data"])

    binance_liquidation_df["time"] = pd.to_datetime(binance_liquidation_df["time"], unit = "ms") # convert unix to date-time

    for col in ["long_liquidation_usd", "short_liquidation_usd"]:
        binance_liquidation_df[col] = pd.to_numeric(binance_liquidation_df[col]) # convert strings to numeric format

    return binance_liquidation_df

