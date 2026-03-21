import pandas as pd 
import numpy as np 

class FeatureEngineer:
    
    @staticmethod
    def create_features(df:pd.DataFrame):

        df = df.copy()

        df["return"] = df["Close"].pct_change()
        df["momentum_5"] = df['Close'].pct_change(5)
        df["sma_10"] = df["Close"].rolling(10).mean()
        df["sma_20"] = df["Close"].rolling(20).mean()
        df["volatility_10"] = df["return"].rolling(10).std()

        #RSI
        delta = df["Close"].diff()
        gain = delta.clip(lower =0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss =loss.rolling(14).mean()
        rs  = avg_gain / avg_loss
        df["RSI"] = 100-(100/(1+rs))

        #Target
        future_return = df["Close"].shift(-5) / df["Close"] - 1

        df["target"] = 0
        df.loc[future_return > 0.01, "target"] = 1
        df.loc[future_return < -0.01, "target"] = -1
        df.dropna(inplace = True)

        return df
    