import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
try:
    from fyers_apiv3 import fyersModel
except ImportError:
    fyersModel = None
from .base_provider import BaseDataProvider


class FyersProvider(BaseDataProvider):

    def __init__(self):
        if fyersModel is None:
            raise ImportError("fyers_apiv3 package is not installed. Please install it to use FyersProvider.")
        load_dotenv()

        self.client_id = os.getenv("FYERS_CLIENT_ID")
        self.access_token = os.getenv("FYERS_ACCESS_TOKEN")

        if not self.client_id or not self.access_token:
            raise ValueError("FYERS credentials missing in .env")

        self.fyers = fyersModel.FyersModel(
            client_id=self.client_id,
            token=self.access_token,
            is_async=False,
            log_path=""
        )

    def _convert_period_to_days(self, period: str) -> int:
        mapping = {
            "1d": 1,
            "5d": 5,
            "1mo": 30,
            "3mo": 90,
            "6mo": 180,
            "1y": 365,
            "2y": 730,
            "5y": 1825
        }
        return mapping.get(period, 365)

    def _convert_interval(self, interval: str) -> str:
        mapping = {
            "1d": "D",
            "1h": "60",
            "30m": "30",
            "15m": "15",
            "5m": "5",
            "1m": "1"
        }
        return mapping.get(interval, "D")

    def get_price_data(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:

        days = self._convert_period_to_days(period)
        resolution = self._convert_interval(interval)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        data = {
            "symbol": ticker,
            "resolution": resolution,
            "date_format": "1",
            "range_from": start_date.strftime("%Y-%m-%d"),
            "range_to": end_date.strftime("%Y-%m-%d"),
            "cont_flag": "1"
        }

        response = self.fyers.history(data)

        if "candles" not in response or not response["candles"]:
            raise ValueError(f"No data fetched for {ticker}")

        df = pd.DataFrame(
            response["candles"],
            columns=["timestamp", "Open", "High", "Low", "Close", "Volume"]
        )

        df["Date"] = pd.to_datetime(df["timestamp"], unit="s")

        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        df = df.dropna(subset=["Close"])
        df = df.sort_values("Date").reset_index(drop=True)

        return df