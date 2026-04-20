from pathlib import Path
from data.providers.fyers_provider import FyersProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY

ticker = "ICICIBANK"

provider = FyersProvider()
file_path = Path(f"data/raw/fyers_{ticker}.csv")

# Load or download data
if file_path.exists():
    print("Loading data from disk")
    data = DataLoader.load_data(f"fyers_{ticker}")
else:
    print("Downloading data from fyers")
    data = provider.get_price_data(f"NSE:{ticker}-EQ")
    DataLoader.save_data(data, f"fyers_{ticker}")

# Load strategy
strategy_class = STRATEGY_REGISTRY["moving_average"]
strategy = strategy_class()

# Generate signals
result = strategy.generate_signals(data)

print(result.tail())