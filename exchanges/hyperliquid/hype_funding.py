
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get funding rates and basis
def get_hype_funding(coin, start_time, end_time):

    # convert time bounds to unix
    start_time_stamp = int(start_time.timestamp() * 1000)
    end_time_stamp = int(end_time.timestamp() * 1000)

    # API call
    url = "https://api.hyperliquid.xyz/info"

    all_hype_funding = []

    while start_time_stamp < end_time_stamp:
        
        payload = {
            "type": "fundingHistory",
            "coin": coin,
            "startTime": start_time_stamp,
            "endTime": end_time_stamp
        }

        response = requests.post(url, json = payload)
        hype_funding = response.json()

        # access all data from pagination
        if len(hype_funding) == 0:
            break

        all_hype_funding.extend(hype_funding)

        last_time = hype_funding[-1]["time"]
        start_time_stamp = last_time + 1

    return all_hype_funding

coin = "BTC"
start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 10th
hype_funding_df = pd.DataFrame(get_hype_funding(coin, start_time, end_time))

# normalize data in dataframe
for col in ["time"]:
    hype_funding_df[col] = pd.to_datetime(hype_funding_df[col], unit="ms", utc=True) # convert unix to date-time
    hype_funding_df[col] = hype_funding_df[col].dt.tz_localize(None) # remove UTC time zone
    
for col in ["fundingRate", "premium"]:
    hype_funding_df[col] = pd.to_numeric(hype_funding_df[col]) # convert strings to numeric format

# plot basis against time
def plot_hype_basis(df: pd.DataFrame):
    
    fig, ax = plt.subplots(figsize = (14, 7))
    ax.plot(hype_funding_df["time"], hype_funding_df["premium"], color = "#0F3933")
    ax.set_xlabel("Time")
    ax.set_ylabel("Basis")

    # x-axis formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.autofmt_xdate()

    # create legend and save the chart
    plt.title("BTC Basis vs. Time")
    plt.savefig("btc_basis_vs_time.png", dpi = 300, bbox_inches = "tight")

# plot funding against time
def plot_hype_funding(df: pd.DataFrame):

    fig, ax = plt.subplots(figsize = (14, 7))
    ax.plot(hype_funding_df["time"], hype_funding_df["fundingRate"], color = "#0F3933")
    ax.set_xlabel("Time")
    ax.set_ylabel("Funding Rate")

    # x-axis formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.autofmt_xdate()

    # y-axis formatting
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: f"{y*100:.3f}%")
    )

    # save the chart
    plt.title("BTC Funding vs. Time")
    plt.savefig("btc_funding_vs_time.png", dpi = 300, bbox_inches = "tight")

plot_hype_funding(hype_funding_df)
plot_hype_basis(hype_funding_df)
