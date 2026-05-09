import pandas as pd
import yfinance as yf
from data.providers.base_provider import BaseDataProvider


class YFinanceProvider(BaseDataProvider):

    def get_price_data(
        self,
        ticker: str,
        period: str = "1d",     # short period for intraday
        interval: str = "1m"    # live-like data
    ) -> pd.DataFrame:

        print(f"YFinance Fetch - {ticker} | {interval}")

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            raise ValueError(f"No data found for {ticker}")

        # =========================
        # FIX MULTI-INDEX (IMPORTANT)
        # =========================
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.reset_index(inplace=True)

        # =========================
        # ENSURE STANDARD FORMAT
        # =========================
        required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]

        df = df[required_cols]

        # =========================
        # FORCE NUMERIC
        # =========================
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        df = df.dropna().reset_index(drop=True)

        print("YFinance cleaned | Rows:", len(df))
        print("Last Candle:", df["Date"].iloc[-1])
        print("Last Price:", df["Close"].iloc[-1])

        return df