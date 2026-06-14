
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get metadata and asset contexts
def get_asset_contexts(dex_name):

    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "metaAndAssetCtxs",
        "dex": dex_name
    }

    response = requests.post(url, json = payload)
    asset_contexts = response.json() # parses JSON data into Python objects

    return asset_contexts

contexts = get_asset_contexts("")

contexts[1][0] # asset context (volume, price, etc.)
contexts[0]["universe"][0] # metadata (asset name, id, etc.)


# get historical price and volume
def get_candle_snapshot(coin, interval):

    # specify time period
    start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
    end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 6th
    start_time_stamp = int(start_time.timestamp() * 1000)
    end_time_stamp = int(end_time.timestamp() * 1000)

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
market_snapshot = get_candle_snapshot(coin, interval) 

snapshot_df = pd.DataFrame(market_snapshot) # convert to dataframe

# normalize data in dataframe
for i in snapshot_df:
    # convert unix to date-time
    snapshot_df["t"] = pd.to_datetime(snapshot_df["t"], unit="ms", utc=True) 
    snapshot_df["T"] = pd.to_datetime(snapshot_df["T"], unit="ms", utc=True)
    # convert strings to numeric format
    snapshot_df["o"] = pd.to_numeric(snapshot_df["o"]) 
    snapshot_df["c"] = pd.to_numeric(snapshot_df["c"])
    snapshot_df["h"] = pd.to_numeric(snapshot_df["h"])
    snapshot_df["l"] = pd.to_numeric(snapshot_df["l"])
    snapshot_df["v"] = pd.to_numeric(snapshot_df["v"])

# remove UTC time zone
snapshot_df["t"] = snapshot_df["t"].dt.tz_localize(None) 
snapshot_df["T"] = snapshot_df["T"].dt.tz_localize(None)

snapshot_df["typical_px"] = (snapshot_df["h"] + snapshot_df["l"] + snapshot_df["c"]) / 3
snapshot_df["ntl_vlm"] = snapshot_df["typical_px"] * snapshot_df["v"]


# plot time on x-axis, typical price and notional volume on y-axis
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(snapshot_df["t"], snapshot_df["typical_px"], color="#F7931A")
ax2.plot(snapshot_df["t"], snapshot_df["ntl_vlm"], color="#000000")
ax1.set_xlabel("Time")
ax1.set_ylabel("Price (USD)")
ax2.set_ylabel("Notional Volume (USD)")

# fix x-axis formatting
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
fig.autofmt_xdate()

# fix right y-axis formatting
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x/1e9:.1f}B")) 

plt.show()


