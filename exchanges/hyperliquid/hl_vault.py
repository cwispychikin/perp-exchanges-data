import requests
import pandas as pd

def hl_vault_pnl(vault_address, period):

    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "vaultDetails",
        "vaultAddress": vault_address
    }

    response = requests.post(url, json = payload)
    vault_info = response.json()

    portfolio = dict(vault_info["portfolio"])
    pnl_history = portfolio[period]["pnlHistory"]

    pnl_df = pd.DataFrame(pnl_history, columns = ["timestamp", "pnl"])

    pnl_df["timestamp"] = pd.to_datetime(pnl_df["timestamp"], unit="ms",)
    pnl_df["pnl"] = pd.to_numeric(pnl_df["pnl"])

    return pnl_df