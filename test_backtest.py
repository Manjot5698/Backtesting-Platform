from pathlib import Path
from analytics.performance_metrics import PerformanceMetrics
from data.providers.fyers_provider import FyersProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine

ticker ="Wipro"
provider = FyersProvider()
file_path = Path(f"data/raw/fyers_{ticker}.csv")
if file_path.exists():
    data = DataLoader.load_data(f"fyers_{ticker}")
else:
    data = provider.get_price_data(f"NSE:{ticker}-EQ")
    DataLoader.save_data(data, f"fyers_{ticker}")

strategy = STRATEGY_REGISTRY["bollinger"]()
data = strategy.generate_signals(data)
engine = BacktestEngine(data,quantity =10)
result = engine.run()
print(result.tail())

print("\nTrades:")
for trade in engine.trades[:5]:
    print(trade.to_dict())

print("\nPerformance Metrics")
print("Total Return:", PerformanceMetrics.total_return(result))
print("Max Drawdown:", PerformanceMetrics.max_drawdown(result))
print("Sharpe Ratio:", PerformanceMetrics.sharpe_ratio(result))
print("Initial Value:", result["portfolio_value"].iloc[0])
print("Final Value:", result["portfolio_value"].iloc[-1])
print("Win Rate:", PerformanceMetrics.win_rate(engine.trades))