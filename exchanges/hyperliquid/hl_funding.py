import requests
import pandas as pd

def hl_funding(token_name_hl, start_time_stamp, end_time_stamp):

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

        # access all paginated data by updating the start_time_stamp to the last time in the response
        if len(hl_funding) == 0:
            break

        all_hl_funding.extend(hl_funding)

        last_time = hl_funding[-1]["time"]

        if last_time <= start_time_stamp:
            break

        start_time_stamp = last_time + 1

    hl_funding_df = pd.DataFrame(all_hl_funding)

    hl_funding_df["time"] = pd.to_datetime(hl_funding_df["time"], unit = "ms") # convert unix to date-time

    for col in ["fundingRate", "premium"]:
        hl_funding_df[col] = pd.to_numeric(hl_funding_df[col]) # convert strings to numeric format

    return hl_funding_df