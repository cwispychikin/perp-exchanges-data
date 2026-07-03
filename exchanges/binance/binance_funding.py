
import requests
import pandas as pd

# get funding rates
def get_binance_funding(token_name_binance, start_time_stamp, end_time_stamp, limit):

    # API call
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": token_name_binance,
        "startTime": start_time_stamp,
        "endTime": end_time_stamp,
        "limit": limit
    }

    response = requests.get(url, params = params)
    binance_funding = response.json()

    return binance_funding

# get basis
def get_binance_basis(token_name_binance, contract_type, interval, limit, start_time_stamp, end_time_stamp):

    # API call
    url = "https://fapi.binance.com/futures/data/basis"
    params = {
        "pair": token_name_binance,
        "contractType": contract_type,
        "period": interval,
        "limit": limit,
        "startTime": start_time_stamp,
        "endTime": end_time_stamp
    }

    response = requests.get(url, params = params)
    binance_basis = response.json()

    return binance_basis

# create dataframes, format data
def build_binance_funding_df(token_name_binance, start_time_stamp, end_time_stamp, limit):

    binance_funding_df = pd.DataFrame(get_binance_funding(token_name_binance, start_time_stamp, end_time_stamp, limit))
    binance_funding_df["fundingTime"] = pd.to_datetime(binance_funding_df["fundingTime"], unit = "ms") # convert unix to date-time

    for col in ["fundingRate", "markPrice"]:
        binance_funding_df[col] = pd.to_numeric(binance_funding_df[col]) # convert strings to numeric format

    return binance_funding_df

def build_binance_basis_df(token_name_binance, contract_type, interval, limit, start_time_stamp, end_time_stamp):

    binance_basis_df = pd.DataFrame(get_binance_basis(token_name_binance, contract_type, interval, limit, start_time_stamp, end_time_stamp))
    binance_basis_df["timestamp"] = pd.to_datetime(binance_basis_df["timestamp"], unit = "ms")

    for col in ["indexPrice", "basisRate", "futuresPrice", "basis"]:
        binance_basis_df[col] = pd.to_numeric(binance_basis_df[col])

    return binance_basis_df
