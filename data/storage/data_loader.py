import pandas as pd
from pathlib import Path


class DataLoader:

    @staticmethod
    def save_data(df: pd.DataFrame, ticker: str):
        file_path = Path(f"data/raw/{ticker}.csv")
        df.to_csv(file_path, index=False)

    @staticmethod
    def load_data(ticker: str) -> pd.DataFrame:
        file_path = Path(f"data/raw/{ticker}.csv")

        df = pd.read_csv(file_path)

        if "Date" not in df.columns:
            raise ValueError("CSV missing 'Date' column")

        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df