
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get historical price and volume
def get_hype_candle(coin, start_time, end_time, interval):

    # convert time bounds to unix
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
    hype_candle = response.json()

    return hype_candle

# price data for BTC
coin = "BTC"
interval = "1h"
start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 10th
hype_candle_df = pd.DataFrame(get_hype_candle(coin, start_time, end_time, interval) ) # convert to dataframe

# normalize data in dataframe
for col in ["t", "T"]:
    hype_candle_df[col] = pd.to_datetime(hype_candle_df[col], unit="ms", utc=True) # convert unix to date-time format
    hype_candle_df[col] = hype_candle_df[col].dt.tz_localize(None) # remove UTC time zone

for col in ["o", "c", "h", "l", "v"]:
    hype_candle_df[col] = pd.to_numeric(hype_candle_df[col]) # convert strings to numeric format

# compute typical price and notional volume
hype_candle_df["typical_px"] = (hype_candle_df["h"] + hype_candle_df["l"] + hype_candle_df["c"]) / 3
hype_candle_df["ntl_vlm"] = hype_candle_df["typical_px"] * hype_candle_df["v"]

# compute volume multiplier
def hype_volume_multiplier(df: pd.DataFrame):

    # filter df between jan. 15th and jan. 29th
    df_jan15_jan29 = df[
        (start_time >= "2026-01-15") &
        (start_time <= "2026-01-29")
    ]

    for _, rows in df_jan15_jan29.iterrows():
        avg_vlm_jan15_jan29 = sum(df_jan15_jan29["ntl_vlm"]) / len(df_jan15_jan29)

    # filter df between jan. 29th and feb. 07th
    df_jan29_feb07 = hype_candle_df[
        (start_time >= "2026-01-29") &
        (start_time <= "2026-02-07")
    ]

    for _, rows in df_jan29_feb07.iterrows():
        avg_vlm_jan29_feb07 = sum(df_jan29_feb07["ntl_vlm"]) / len(df_jan29_feb07)

    # compute volume multiplier
    volume_multiplier = avg_vlm_jan29_feb07 / avg_vlm_jan15_jan29
    return volume_multiplier

# plot price and notional volume against time
def plot_hype_price_volume(df: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize = (14, 7))
    ax2 = ax1.twinx()

    ax1.plot(start_time, hype_candle_df["typical_px"], color="#F7931A", label = "Typical Price")
    ax2.plot(start_time, hype_candle_df["ntl_vlm"], color="#0F3933", label = "Notional Volume")
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

