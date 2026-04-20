from pathlib import Path
import pandas as pd

from data.providers.yfinance_provider import YFinanceProvider
from data.providers.fyers_provider import FyersProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from ml.pipeline import MLPipeline
from analytics.performance_metrics import PerformanceMetrics


# =========================
# CONFIG
# =========================
PROVIDER = "fyers"   # "yfinance" or "fyers"

TICKER = "ICICIBANK"  # base ticker (no suffix)

MODE = "moving_average"
# options:
# "ml"
# "moving_average"
# "rsi"
# "bollinger"


# =========================
# PROVIDER SETUP
# =========================
if PROVIDER == "yfinance":
    provider = YFinanceProvider()
    ticker_formatted = f"{TICKER}.NS"

elif PROVIDER == "fyers":
    provider = FyersProvider()
    ticker_formatted = f"NSE:{TICKER}-EQ"

else:
    raise ValueError("Invalid provider selected")


# =========================
# LOAD DATA
# =========================
file_path = Path(f"data/raw/{PROVIDER}_{TICKER}.csv")

if file_path.exists():
    print(f"{TICKER} → loaded from disk ({PROVIDER})")
    df = DataLoader.load_data(f"{PROVIDER}_{TICKER}")
else:
    print(f"{TICKER} → downloading from {PROVIDER}")
    df = provider.get_price_data(ticker_formatted)
    DataLoader.save_data(df, f"{PROVIDER}_{TICKER}")


# =========================
# GENERATE SIGNALS
# =========================
if MODE == "bollinger":

    pipeline = MLPipeline()
    data = pipeline.run(df)

else:

    strategy_class = STRATEGY_REGISTRY[MODE]
    strategy = strategy_class()

    data = strategy.generate_signals(df)


# =========================
# BACKTEST
# =========================
engine = BacktestEngine(data, quantity=10)
result = engine.run()


# =========================
# OUTPUT
# =========================
print("\nFinal Data:")
print(result.tail())

print("\nTrades:")
for trade in engine.trades[:5]:
    print(trade.to_dict())

print("\nPerformance Metrics")
print("Total Return:", PerformanceMetrics.total_return(result))
print("Max Drawdown:", PerformanceMetrics.max_drawdown(result))
print("Sharpe Ratio:", PerformanceMetrics.sharpe_ratio(result))
print("Win Rate:", PerformanceMetrics.win_rate(engine.trades))

print("\nInitial Value:", result["portfolio_value"].iloc[0])
print("Final Value:", result["portfolio_value"].iloc[-1])