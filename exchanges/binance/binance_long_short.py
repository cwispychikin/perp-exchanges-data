import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../coinglass_api_key.env")
coinglass_api_key = os.getenv("COINGLASS_API_KEY")

if coinglass_api_key is None:
    raise ValueError("COINGLASS_API_KEY not loaded")

# get global account long/short ratio
def get_binance_global_account_long_short(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    # API call
    url = "https://open-api-v4.coinglass.com/api/futures/global-long-short-account-ratio/history"
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
    binance_global_account_long_short = response.json()

    return binance_global_account_long_short

# get top account long/short ratio
def get_binance_top_account_long_short(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    # API call
    url = "https://open-api-v4.coinglass.com/api/futures/top-long-short-account-ratio/history"
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
    binance_top_account_long_short = response.json()

    return binance_top_account_long_short

# create dataframe, format data
def build_binance_global_account_long_short_df(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    binance_global_account_long_short = get_binance_global_account_long_short(cg_token_name_binance, interval, start_time_stamp, end_time_stamp)
    binance_global_account_long_short_df = pd.DataFrame(binance_global_account_long_short["data"])

    binance_global_account_long_short_df["time"] = pd.to_datetime(binance_global_account_long_short_df["time"], unit = "ms") # convert unix to date-time

    for col in ["global_account_long_percent", "global_account_short_percent", "global_account_long_short_ratio"]:
        binance_global_account_long_short_df[col] = pd.to_numeric(binance_global_account_long_short_df[col]) # convert strings to numeric format

    return binance_global_account_long_short_df

def build_binance_top_account_long_short_df(cg_token_name_binance, interval, start_time_stamp, end_time_stamp):

    binance_top_account_long_short = get_binance_top_account_long_short(cg_token_name_binance, interval, start_time_stamp, end_time_stamp)
    binance_top_account_long_short_df = pd.DataFrame(binance_top_account_long_short["data"])

    binance_top_account_long_short_df["time"] = pd.to_datetime(binance_top_account_long_short_df["time"], unit = "ms") # convert unix to date-time

    for col in ["top_account_long_percent", "top_account_short_percent", "top_account_long_short_ratio"]:
        binance_top_account_long_short_df[col] = pd.to_numeric(binance_top_account_long_short_df[col]) # convert strings to numeric format

    return binance_top_account_long_short_df