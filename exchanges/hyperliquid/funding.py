
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get funding rates
def get_funding_rates(coin):

    # specify time period
    start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
    end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 10th
    start_time_stamp = int(start_time.timestamp() * 1000)
    end_time_stamp = int(end_time.timestamp() * 1000)

    # API call
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "fundingHistory",
        "coin": coin,
        "startTime": start_time_stamp,
        "endTime": end_time_stamp
    }

    response = requests.post(url, json = payload)
    funding_rates = response.json()

    return funding_rates

coin = "BTC"
historical_funding_rates = get_funding_rates(coin)
funding_df = pd.DataFrame(historical_funding_rates)

# normalize data in dataframe
for col in ["time"]:
    funding_df[col] = pd.to_datetime(funding_df[col], unit="ms", utc=True) # convert unix to date-time
    funding_df[col] = funding_df[col].dt.tz_localize(None) # remove UTC time zone
    
for col in ["fundingRate", "premium"]:
    funding_df[col] = pd.to_numeric(funding_df[col]) # convert strings to numeric format

# assign columns to variables
funding_rate = funding_df["fundingRate"] 
premium = funding_df["premium"]
time = funding_df["time"]

# plot premium against time
def premium_chart(df: pd.DataFrame):
    
    fig, ax = plt.subplots(figsize = (14, 7))
    ax.plot(time, premium, color = "#0F3933", label = "Premium")
    ax.plot(time, funding_rate, color = "#F7931A", label = "Funding Rate")
    ax.set_xlabel("Time")
    ax.set_ylabel("Premium")

    # fix x-axis formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.autofmt_xdate()

    # create legend and save the chart
    ax.legend()
    plt.title("BTC Premium vs. Time")
    plt.savefig("btc_premium_funding_vs_time.png", dpi=300, bbox_inches="tight")
