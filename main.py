from pathlib import Path

from data.providers.fyers_provider import FyersProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from analytics.performance_metrics import PerformanceMetrics


# =========================
# CONFIG
# =========================
TICKER = "RELIANCE"

MODE = "moving_average"
# options:
# "moving_average"
# "rsi"
# "bollinger"


# =========================
# LOAD DATA
# =========================
provider = FyersProvider()
file_path = Path(f"data/raw/{TICKER}.csv")

if file_path.exists():
    print(f"{TICKER} - loaded from disk")
    df = DataLoader.load_data(TICKER)
else:
    print(f"{TICKER} - fetching from FYERS")
    df = provider.get_price_data(TICKER)

    if df.empty:
        raise ValueError(f"No data returned for {TICKER}")

    DataLoader.save_data(df, TICKER)


# =========================
# STRATEGY SELECTION
# =========================
strategy_class = STRATEGY_REGISTRY[MODE]
strategy = strategy_class()


# =========================
# BACKTEST
# =========================
engine = BacktestEngine(df, strategy=strategy, quantity=10)
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