import pandas as pd
from .base_strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):

    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:

        df = data.copy()

        # =========================
        # INDICATORS
        # =========================
        df["SMA_short"] = df["Close"].rolling(self.short_window).mean()
        df["SMA_long"] = df["Close"].rolling(self.long_window).mean()

        # =========================
        # SIGNALS
        # =========================
        df["signal"] = 0

        df.loc[
            (df["SMA_short"] > df["SMA_long"]) &
            (df["SMA_short"].shift(1) <= df["SMA_long"].shift(1)),
            "signal"
        ] = 1

        df.loc[
            (df["SMA_short"] < df["SMA_long"]) &
            (df["SMA_short"].shift(1) >= df["SMA_long"].shift(1)),
            "signal"
        ] = -1

        # 🔥 Fill signals properly
        df["signal"] = df["signal"].replace(0, pd.NA).ffill()
        df["signal"] = df["signal"].fillna(0)
        df["signal"] = df["signal"].infer_objects(copy=False).astype(int)

        return df