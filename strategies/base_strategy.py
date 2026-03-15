import pandas as pd 
from abc import ABC, abstractmethod

class BaseStrategy(ABC):

    @abstractmethod
    def generate_signals(self,data:pd.DataFrame)->pd.DataFrame:
        """
        Takes OHLCV data and returns a dataframe with a 'signal' column.
        signal values:
        1 -> Buy
        -1 -> Sell
        0 -> Hold
        """
        pass