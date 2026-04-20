from fyers_apiv3 import fyersModel

fyers = fyersModel.FyersModel(
    client_id="PK6ZJD5VET-100",
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIl0sImF0X2hhc2giOiJnQUFBQUFCcDVhTjREdk5mRldpTXgtQXBxRjJpUVZSQng0RmotODJkMXNmSDZSakhiN0phazJhMWxmeEh4d0dPWE9ZeWVITDF1cDhoekdBVGlFU2FmVmdBaWs4NDhLeWtucnBEdFR6MnhGb3B2X2NoY2Z0YXR1dz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJmNTgyNDVjNGUwYjI1ZTNhYjYzNjgwNDAwYWNjN2YzYTI2OTBmNDM1MWQwMmFmZjU5MDRhOTUzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiRkFKMzQ0NjciLCJhcHBUeXBlIjoxMDAsImV4cCI6MTc3NjczMTQwMCwiaWF0IjoxNzc2NjU3MjcyLCJpc3MiOiJhcGkuZnllcnMuaW4iLCJuYmYiOjE3NzY2NTcyNzIsInN1YiI6ImFjY2Vzc190b2tlbiJ9.d2fIpn9OaoefpdPxol14gsHikIMwfwjYanNDzSEAQUI",
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