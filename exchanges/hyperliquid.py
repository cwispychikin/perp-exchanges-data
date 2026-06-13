
import requests
import json

def get_data(type, dex_name):

    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": type,
        "dex": dex_name
    }

    response = requests.post(url, json = payload)
    contexts = response.json() # parses JSON data into Python objects

    return contexts


data = get_data("metaAndAssetCtxs", "")
print(data[1][0])
print(data[0]["universe"][0])


