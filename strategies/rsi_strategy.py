import pandas as pd
from strategies.base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):

    def __init__(self, period=14, lower=30, upper=70):
        self.period = period
        self.lower = lower
        self.upper = upper

    def generate_signals(self, data: pd.DataFrame):

        df = data.copy()

        # =========================
        # RSI (EMA-based)
        # =========================
        delta = df["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(span=self.period, adjust=False).mean()
        avg_loss = loss.ewm(span=self.period, adjust=False).mean()

        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # =========================
        # RAW SIGNALS (CROSSOVER)
        # =========================
        df["signal"] = 0

        # BUY when RSI crosses ABOVE lower threshold
        df.loc[
            (df["RSI"] > self.lower) &
            (df["RSI"].shift(1) <= self.lower),
            "signal"
        ] = 1

        # SELL when RSI crosses BELOW upper threshold
        df.loc[
            (df["RSI"] < self.upper) &
            (df["RSI"].shift(1) >= self.upper),
            "signal"
        ] = -1

        # =========================
        # PERSIST POSITION (FIXED)
        # =========================
        df["signal"] = df["signal"].replace(0, pd.NA).ffill()
        df["signal"] = df["signal"].fillna(0)

        return df