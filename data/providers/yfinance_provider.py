import yfinance as yf
import pandas as pd
from .base_provider import BaseDataProvider


class YFinanceProvider(BaseDataProvider):

    def get_price_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            raise ValueError(f"No data fetched for {ticker}")

        # flatten columns if multi-index
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.columns.name = None

        df.dropna(inplace=True)

        # convert index to column
        df.reset_index(inplace=True)

        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df["Date"] = pd.to_datetime(df["Date"])

        df = df.sort_values("Date").reset_index(drop=True)

        return df