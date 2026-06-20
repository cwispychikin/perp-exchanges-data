
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get historical price and volume
def get_hype_candle(coin, start_time, end_time, interval):

    # convert time bounds to utx format
    start_time_stamp = int(start_time.timestamp() * 1000)
    end_time_stamp = int(end_time.timestamp() * 1000)

    # API call
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin, # prefix with DEX name (e.g., xyz:XYZ100)
            "interval": interval,
            "startTime": start_time_stamp,
            "endTime": end_time_stamp
        }
    }

    response = requests.post(url, json = payload)
    candle_snapshot = response.json()

    return candle_snapshot

# price data for BTC
coin = "BTC"
interval = "1h"
start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 10th
market_snapshot = get_hype_candle(coin, start_time, end_time, interval) 

snapshot_df = pd.DataFrame(market_snapshot) # convert to dataframe

# normalize data in dataframe
for col in ["t", "T"]:
    snapshot_df[col] = pd.to_datetime(snapshot_df[col], unit="ms", utc=True) # convert unix to date-time format
    snapshot_df[col] = snapshot_df[col].dt.tz_localize(None) # remove UTC time zone

for col in ["o", "c", "h", "l", "v"]:
    snapshot_df[col] = pd.to_numeric(snapshot_df[col]) # convert strings to numeric format

# assign columns to variables
start_time = snapshot_df["t"]
end_time = snapshot_df["T"]
open = snapshot_df["o"]
close = snapshot_df["c"]
high = snapshot_df["h"]
low = snapshot_df["l"]
volume = snapshot_df["v"]

# compute typical price and notional volume, assign to variables
snapshot_df["typical_px"] = (high + low + close) / 3
typical_px = snapshot_df["typical_px"]
snapshot_df["ntl_vlm"] = snapshot_df["typical_px"] * volume
notional_volume = snapshot_df["ntl_vlm"]

# compute volume multiplier
def hype_volume_multiplier(df: pd.DataFrame):

    # filter df between jan. 15th and jan. 29th
    snapshot_jan15_jan29 = df[
        (start_time >= "2026-01-15") &
        (start_time <= "2026-01-29")
    ]

    for _, rows in snapshot_jan15_jan29.iterrows():
        avg_vlm_jan15_jan29 = sum(snapshot_jan15_jan29["ntl_vlm"]) / len(snapshot_jan15_jan29)

    # filter df between jan. 29th and feb. 07th
    snapshot_jan29_feb07 = snapshot_df[
        (start_time >= "2026-01-29") &
        (start_time <= "2026-02-07")
    ]

    for _, rows in snapshot_jan29_feb07.iterrows():
        avg_vlm_jan29_feb07 = sum(snapshot_jan29_feb07["ntl_vlm"]) / len(snapshot_jan29_feb07)

    # compute volume multiplier
    volume_multiplier = avg_vlm_jan29_feb07 / avg_vlm_jan15_jan29
    return volume_multiplier


# plot price and notional volume against time
def plot_hype_price_volume(df: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize = (14, 7))
    ax2 = ax1.twinx()

    ax1.plot(start_time, typical_px, color="#F7931A", label = "Typical Price")
    ax2.plot(start_time, notional_volume, color="#0F3933", label = "Notional Volume")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Price (USD)")
    ax2.set_ylabel("Notional Volume (USD)")

    # x-axis formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.autofmt_xdate()

    # right y-axis formatting
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x/1e9:.1f}B")) 

    # create legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
    handles1 + handles2,
    labels1 + labels2
    )

    # save the chart
    plt.title("BTC Price & Notional Volume vs. Time")
    plt.savefig("btc_price_vlm_vs_time.png", dpi=300, bbox_inches="tight")

