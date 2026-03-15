from pathlib import Path
from data.providers.yfinance_provider import YFinanceProvider
from data.storage.data_loader import DataLoader

TICKERS = ["ICICIBANK.NS", "HDFCBANK.NS"]

provider = YFinanceProvider()

for ticker in TICKERS:

    file_path = Path(f"data/raw/{ticker}.csv")

    if file_path.exists():
        print(f"{ticker} → loaded from disk")
        df = DataLoader.load_data(ticker)

    else:
        print(f"{ticker} → downloading from yfinance")
        df = provider.get_price_data(ticker)
        DataLoader.save_data(df, ticker)

    print(df.tail())