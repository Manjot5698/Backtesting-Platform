import pandas as pd
from .base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):

    def __init__(self,short_window =20,long_window =50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self,data:pd.DataFrame)->pd.DataFrame:
        df = data.copy()

        df["SMA_short"] = df["Close"].rolling(self.short_window).mean()
        df["SMA_long"] = df["Close"].rolling(self.long_window).mean()

        df["signal"] = 0

        df.loc[df["SMA_short"]>df["SMA_long"],"signal"] =1
        df.loc[df["SMA_short"]<df["SMA_long"],"signal"] =-1
        
        return df