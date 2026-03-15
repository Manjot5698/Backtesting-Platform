import pandas as pd 
from pathlib import Path

DATA_DIR = Path('data/raw')
DATA_DIR.mkdir(parents = True,exist_ok =True)

class DataLoader:
    @staticmethod
    def save_data(df:pd.dataFrame,ticker:str):
        file_path = DATA_DIR / f"{ticker}.csv"
        df.to_csv(file_path,index =False)

    @staticmethod
    def load_data(ticker:str)->pd.DataFrame:
        file_path = DATA_DIR / f"{ticker}.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"No data found for {ticker}")
        return pd.read_csv(file_path)