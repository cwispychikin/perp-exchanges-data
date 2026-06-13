
import requests
import json
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
    start_time = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)
    end_time = datetime(2026, 2, 6, 0, 0, 0, tzinfo=timezone.utc)
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

coin = "BTC"
interval = "8h"
market_snapshot = get_candle_snapshot(coin, interval)
print(json.dumps(market_snapshot, indent=4))

