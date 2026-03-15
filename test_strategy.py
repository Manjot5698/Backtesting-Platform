from pathlib import Path
from data.providers.yfinance_provider import YFinanceProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY

ticker = "ICICIBANK.NS"

provider = YFinanceProvider()
file_path = Path(f"data/raw/{ticker}.csv")

# Load or download data
if file_path.exists():
    print("Loading data from disk")
    data = DataLoader.load_data(ticker)
else:
    print("Downloading data from yfinance")
    data = provider.get_price_data(ticker)
    DataLoader.save_data(data, ticker)

# Load strategy
strategy_class = STRATEGY_REGISTRY["moving_average"]
strategy = strategy_class()

# Generate signals
result = strategy.generate_signals(data)

print(result.tail())