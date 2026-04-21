import pandas as pd
from pathlib import Path

# 📁 Data directory
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


class DataLoader:

    @staticmethod
    def save_data(df: pd.DataFrame, ticker: str):
        """
        Save dataframe to CSV
        """
        file_path = DATA_DIR / f"{ticker}.csv"
        df.to_csv(file_path, index=False)

    @staticmethod
    def load_data(ticker: str) -> pd.DataFrame:
        """
        Load CSV data for ticker
        """
        file_path = DATA_DIR / f"{ticker}.csv"

        if not file_path.exists():
            raise FileNotFoundError(f"❌ No data found for {ticker}")

        df = pd.read_csv(file_path, parse_dates=["Date"])

        # ✅ Sort data (important for backtesting)
        df = df.sort_values(by="Date")

        return df