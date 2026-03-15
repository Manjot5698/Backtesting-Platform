from abc import ABC,abstractmethod
import pandas as pd
class BaseDataProvider(ABC):

    @abstractmethod
    def get_price_data(self,ticker:str,period:str,interval:str,)->pd.DataFrame:
        '''
        Fetches  historical market data.
        Must return a Dataframe with columns:
        Date,Open,High,Low,Close,Volume
        '''
        pass