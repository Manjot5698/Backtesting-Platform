from data.providers.fyers_provider import FyersProvider
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from analytics.performance_metrics import PerformanceMetrics


# =========================
# CONFIG
# =========================
TICKER = "RELIANCE"
PERIOD = "5d"  # options: "1d", "5d", "1mo", "3mo", "6mo", "1y"
INTERVAL = "5m"  # options: "1m", "5m", "15m", "30m", "1h", "1d"

MODE = "moving_average"
# options:
# "moving_average"
# "rsi"
# "bollinger"


# =========================
# LOAD DATA
# =========================
provider = FyersProvider()

print(f"{TICKER} - fetching from FYERS (period: {PERIOD}, interval: {INTERVAL})")
df = provider.get_price_data(TICKER, period=PERIOD, interval=INTERVAL)

if df.empty:
    raise ValueError(f"No data returned for {TICKER}")


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