import pandas as pd
from strategies.base_strategy import BaseStrategy


class BollingerStrategy(BaseStrategy):

    def __init__(self, window=20):
        self.window = window

    def generate_signals(self, data: pd.DataFrame):

        df = data.copy()

        # =========================
        # INDICATORS
        # =========================
        df["MA"] = df["Close"].rolling(self.window).mean()
        df["STD"] = df["Close"].rolling(self.window).std()

        df["upper_band"] = df["MA"] + 2 * df["STD"]
        df["lower_band"] = df["MA"] - 2 * df["STD"]

        # =========================
        # RAW SIGNALS
        # =========================
        df["signal"] = 0

        df.loc[df["Close"] < df["lower_band"], "signal"] = 1   # BUY
        df.loc[df["Close"] > df["upper_band"], "signal"] = -1  # SELL

        # =========================
        # PERSIST POSITION (FIXED)
        # =========================
        df["signal"] = df["signal"].replace(0, pd.NA).ffill()
        df["signal"] = df["signal"].fillna(0)

        # Optional: clean integers
        df["signal"] = df["signal"].astype(int)

        return df