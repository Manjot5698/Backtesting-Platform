from pathlib import Path
import pandas as pd

from data.providers.yfinance_provider import YFinanceProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from ml.pipeline import MLPipeline
from analytics.performance_metrics import PerformanceMetrics


# =========================
# CONFIG
# =========================
TICKER = "ICICIBANK.NS"

MODE = "moving_average"  
# options:
# "ml"
# "moving_average"
# "rsi"
# "bollinger"


# =========================
# LOAD DATA
# =========================
provider = YFinanceProvider()
file_path = Path(f"data/raw/{TICKER}.csv")

if file_path.exists():
    print(f"{TICKER} → loaded from disk")
    df = DataLoader.load_data(TICKER)
else:
    print(f"{TICKER} → downloading from yfinance")
    df = provider.get_price_data(TICKER)
    DataLoader.save_data(df, TICKER)


# =========================
# GENERATE SIGNALS
# =========================
if MODE == "ml":

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