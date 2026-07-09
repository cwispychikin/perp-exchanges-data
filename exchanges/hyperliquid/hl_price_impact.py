import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv("../dune_api_key.env")
dune_api_key = os.getenv("DUNE_API_KEY")

if dune_api_key is None:
    raise ValueError("DUNE_API_KEY not loaded")

# fetch price impact data from Dune Analytics
def hl_price_impact(query_id):

    headers = {
        "X-Dune-API-Key": dune_api_key
    }

    # execute query
    execute_url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    execute_response = requests.post(execute_url, headers = headers)
    execute_response.raise_for_status()

    execution_id = execute_response.json()["execution_id"]

    # wait for completion
    status_url = f"https://api.dune.com/api/v1/execution/{execution_id}/status"

    while True:
        status_response = requests.get(status_url, headers = headers)
        status_response.raise_for_status()

        status_data = status_response.json()
        state = status_data["state"]

        if state == "QUERY_STATE_COMPLETED":
            break

        if state in ["QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED"]:
            raise ValueError(status_data)

        time.sleep(5)

    # fetch results
    results_url = f"https://api.dune.com/api/v1/execution/{execution_id}/results"
    hl_price_impact = requests.get(results_url, headers = headers)
    hl_price_impact.raise_for_status()

    rows = hl_price_impact.json()["result"]["rows"]

    hl_price_impact_df = pd.DataFrame(rows)
    hl_price_impact_df["time"] = pd.to_datetime(hl_price_impact_df["time"])

    for col in ["mid_px", "impact_bid_px", "impact_ask_px"]:
        hl_price_impact_df[col] = pd.to_numeric(hl_price_impact_df[col])

    return hl_price_impact_df