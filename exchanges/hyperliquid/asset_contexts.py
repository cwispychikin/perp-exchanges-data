
import requests
import json
import pandas as pd

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