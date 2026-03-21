import pandas as pd
from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Takes OHLCV data and returns a dataframe with a 'signal' column.

        signal values:
        1 -> Buy
        -1 -> Sell
        0 -> Hold
        """
        pass

    def validate(self, df: pd.DataFrame):

        required_cols = {"Date", "Open", "High", "Low", "Close", "Volume"}

        if not required_cols.issubset(df.columns):
            raise ValueError("Input data missing required OHLCV columns")

        if "signal" not in df.columns:
            raise ValueError("Output must contain 'signal' column")

        if not set(df["signal"].dropna().unique()).issubset({-1, 0, 1}):
            raise ValueError("Signal values must be in {-1, 0, 1}")