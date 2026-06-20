
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timezone

# get funding rates
def get_binance_funding(coin, start_time, end_time, limit):

    # convert time bounds to unix
    start_time_stamp = int(start_time.timestamp() * 1000)
    end_time_stamp = int(end_time.timestamp() * 1000)

    # API call
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": coin,
        "startTime": start_time_stamp,
        "endTime": end_time_stamp, 
        "limit": limit
    }

    response = requests.get(url, params = params)
    binance_funding = response.json()

    return binance_funding

coin = "BTCUSDT"
start_time = datetime(2026, 1, 15, 0, 0, 0, tzinfo=timezone.utc) # start date: jan 15th
end_time = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc) # end date: feb 10th
limit = 1000

binance_funding_df = pd.DataFrame(get_binance_funding(coin, start_time, end_time, limit))

# normalize data in dataframe
for col in ["fundingTime"]:
    binance_funding_df[col] = pd.to_datetime(binance_funding_df[col], unit="ms", utc=True) # convert unix to date-time
    binance_funding_df[col] = binance_funding_df[col].dt.tz_localize(None) # remove UTC time zone
    
for col in ["fundingRate", "markPrice"]:
    binance_funding_df[col] = pd.to_numeric(binance_funding_df[col]) # convert strings to numeric format

print(binance_funding_df)



# get basis















