import pandas as pd 
from strategies.base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self,period =14):
        self.period = period
    
    def generate_signals(self, data: pd.DataFrame):
        df = data.copy()

        delta =df["Close"].diff()
        gain = delta.clip(lower = 0)
        loss  = -delta.clip(upper =0)
        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()
        rs = avg_gain/avg_loss
        df["RSI"] = 100 - (100/(1+rs))
        df["signal"] = 0
        df.loc[df["RSI"]<30,"signal"] =1
        df.loc[df["RSI"]>70,"signal"] =-1

        return df