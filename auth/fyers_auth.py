from fyers_apiv3 import fyersModel
import os

fyers = fyersModel.FyersModel(
    client_id=os.getenv("FYERS_CLIENT_ID"),
    token=os.getenv("FYERS_ACCESS_TOKEN"),
    is_async=False
)

data = {
    "symbol": "NSE:RELIANCE-EQ",
    "resolution": "D",
    "date_format": "1",
    "range_from": "2023-01-01",
    "range_to": "2023-12-31",
    "cont_flag": "1"
}

response = fyers.history(data)
import pandas as pd

candles = response["candles"]

df = pd.DataFrame(
    candles,
    columns=["timestamp", "open", "high", "low", "close", "volume"]
)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df.set_index("timestamp", inplace=True)

print(df.head())

print(response)