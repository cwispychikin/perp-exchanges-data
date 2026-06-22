
import requests
import pandas as pd

# get funding rates and basis
def get_hl_funding(token_name_hl, start_time_stamp, end_time_stamp):

    # API call
    url = "https://api.hyperliquid.xyz/info"

    all_hl_funding = []

    while start_time_stamp < end_time_stamp:

        payload = {
            "type": "fundingHistory",
            "coin": token_name_hl,
            "startTime": start_time_stamp,
            "endTime": end_time_stamp
        }

        response = requests.post(url, json = payload)
        hl_funding = response.json()

        # access all data from pagination
        if len(hl_funding) == 0:
            break

        all_hl_funding.extend(hl_funding)

        last_time = hl_funding[-1]["time"]
        start_time_stamp = last_time + 1

    return all_hl_funding

# create & normalize data in hyperliquid funding dataframe
def build_hl_funding_df(token_name_hl, start_time_stamp, end_time_stamp):

    hl_funding_df = pd.DataFrame(get_hl_funding(token_name_hl, start_time_stamp, end_time_stamp))

    hl_funding_df["time"] = pd.to_datetime(hl_funding_df["time"], unit="ms") # convert unix to date-time

    for col in ["fundingRate", "premium"]:
        hl_funding_df[col] = pd.to_numeric(hl_funding_df[col]) # convert strings to numeric format

    return hl_funding_df

# transform funding into an 8h interval dataframe to match binance data
def build_hl_8h_funding_df(hl_funding_df: pd.DataFrame):

    hl_8h_funding_df = (
        hl_funding_df
        .set_index("time")
        .resample("8h")["fundingRate"]
        .sum()
        .reset_index(name="fundingRate")
    )

    return hl_8h_funding_df
