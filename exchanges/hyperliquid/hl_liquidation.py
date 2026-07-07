import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../coinglass_api_key.env")
coinglass_api_key = os.getenv("COINGLASS_API_KEY")

if coinglass_api_key is None:
    raise ValueError("COINGLASS_API_KEY not loaded")

# get liquidation
def get_hl_liquidation(cg_token_name_hl, interval, start_time_stamp, end_time_stamp):

    # API call
    url = "https://open-api-v4.coinglass.com/api/futures/liquidation/history"
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
    hl_liquidation = response.json()

    return hl_liquidation

# create dataframe, format data
def build_hl_liquidation_df(cg_token_name_hl, interval, start_time_stamp, end_time_stamp):

    hl_liquidation = get_hl_liquidation(cg_token_name_hl, interval, start_time_stamp, end_time_stamp)
    hl_liquidation_df = pd.DataFrame(hl_liquidation["data"])

    hl_liquidation_df["time"] = pd.to_datetime(hl_liquidation_df["time"], unit = "ms") # convert unix to date-time

    for col in ["long_liquidation_usd", "short_liquidation_usd"]:
        hl_liquidation_df[col] = pd.to_numeric(hl_liquidation_df[col]) # convert strings to numeric format

    return hl_liquidation_df

