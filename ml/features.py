import pandas as pd 
import numpy as np 

class FeatureEngineer:
    
    @staticmethod
    def create_features(df: pd.DataFrame):
        """Create technical analysis features for ML model"""
        
        df = df.copy()

        # Basic returns and momentum
        df["return"] = df["Close"].pct_change()
        df["momentum_5"] = df['Close'].pct_change(5)
        df["momentum_10"] = df['Close'].pct_change(10)
        
        # Moving averages
        df["sma_10"] = df["Close"].rolling(10).mean()
        df["sma_20"] = df["Close"].rolling(20).mean()
        df["sma_50"] = df["Close"].rolling(50).mean()
        
        # EMA
        df["ema_12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["ema_26"] = df["Close"].ewm(span=26, adjust=False).mean()
        
        # Volatility
        df["volatility_10"] = df["return"].rolling(10).std()
        df["volatility_20"] = df["return"].rolling(20).std()
        
        # MACD
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["signal_line"] = df["macd"].ewm(span=9, adjust=False).mean()
        df["macd_histogram"] = df["macd"] - df["signal_line"]

        # RSI (Relative Strength Index)
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df["bb_middle"] = df["Close"].rolling(20).mean()
        bb_std = df["Close"].rolling(20).std()
        df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
        df["bb_lower"] = df["bb_middle"] - (bb_std * 2)
        df["bb_position"] = (df["Close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])
        
        # ATR (Average True Range)
        df["high_low"] = df["High"] - df["Low"]
        df["high_close"] = abs(df["High"] - df["Close"].shift())
        df["low_close"] = abs(df["Low"] - df["Close"].shift())
        df["tr"] = df[["high_low", "high_close", "low_close"]].max(axis=1)
        df["atr"] = df["tr"].rolling(14).mean()
        
        # Volume features (if available)
        if "Volume" in df.columns:
            df["volume_sma"] = df["Volume"].rolling(20).mean()
            df["volume_ratio"] = df["Volume"] / df["volume_sma"]
        
        # Price position
        df["high_20"] = df["Close"].rolling(20).max()
        df["low_20"] = df["Close"].rolling(20).min()
        df["price_position"] = (df["Close"] - df["low_20"]) / (df["high_20"] - df["low_20"])

        # Target: Future return (5 days ahead)
        future_return = df["Close"].shift(-5) / df["Close"] - 1

        df["target"] = 0
        df.loc[future_return > 0.01, "target"] = 1    # Buy signal
        df.loc[future_return < -0.01, "target"] = -1  # Sell signal
        
        # Remove NaN values
        df.dropna(inplace=True)

        return df
    