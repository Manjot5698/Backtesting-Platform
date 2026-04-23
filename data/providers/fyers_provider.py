import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

from data.providers.base_provider import BaseDataProvider


class FyersProvider(BaseDataProvider):

    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("FYERS_CLIENT_ID")
        self.access_token = os.getenv("FYERS_ACCESS_TOKEN")

        if not self.client_id or not self.access_token:
            raise ValueError("❌ FYERS credentials missing in .env")

        self.fyers = fyersModel.FyersModel(
            client_id=self.client_id,
            token=self.access_token,
            is_async=False,
            log_path=""
        )

    # =========================
    # SYMBOL FORMAT FIX
    # =========================
    def _format_symbol(self, ticker: str) -> str:
        ticker = ticker.upper().replace(".NS", "")
        return f"NSE:{ticker}-EQ"

    # =========================
    # PERIOD → DAYS
    # =========================
    def _convert_period_to_days(self, period: str) -> int:
        mapping = {
            "1d": 1,
            "5d": 5,
            "1mo": 30,
            "3mo": 90,
            "6mo": 180,
            "1y": 365
        }
        return mapping.get(period, 5)

    # =========================
    # INTERVAL → FYERS RESOLUTION
    # =========================
    def _convert_interval(self, interval: str) -> str:
        mapping = {
            "1d": "D",
            "1h": "60",
            "30m": "30",
            "15m": "15",
            "5m": "5",
            "1m": "1"
        }
        return mapping.get(interval, "5")  # 🔥 default 5m

    # =========================
    # MAIN FETCH
    # =========================
    def get_price_data(
        self,
        ticker: str,
        period: str = "5d",      # 🔥 shorter for live feel
        interval: str = "5m"     # 🔥 intraday
    ) -> pd.DataFrame:

        symbol = self._format_symbol(ticker)

        days = self._convert_period_to_days(period)
        resolution = self._convert_interval(interval)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        payload = {
            "symbol": symbol,
            "resolution": resolution,
            "date_format": "1",
            "range_from": start_date.strftime("%Y-%m-%d"),
            "range_to": end_date.strftime("%Y-%m-%d"),
            "cont_flag": "1"
        }

        print(f"📡 FYERS Fetch → {symbol} | {resolution}")

        response = self.fyers.history(data=payload)

        # =========================
        # ERROR HANDLING
        # =========================
        if response.get("s") != "ok":
            print("❌ FYERS ERROR:", response)
            raise ValueError(f"FYERS API Error: {response}")

        candles = response.get("candles", [])

        if not candles:
            raise ValueError(f"❌ No data fetched for {ticker}")

        # =========================
        # DATAFRAME
        # =========================
        df = pd.DataFrame(
            candles,
            columns=["timestamp", "Open", "High", "Low", "Close", "Volume"]
        )

        df["Date"] = pd.to_datetime(df["timestamp"], unit="s")

        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # =========================
        # CLEAN TYPES
        # =========================
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna().reset_index(drop=True)

        print(f"✅ FYERS SUCCESS | Rows: {len(df)}")
        print("📅 Last Candle:", df["Date"].iloc[-1])
        print("💰 Last Price:", df["Close"].iloc[-1])

        return df