from pathlib import Path
from analytics.performance_metrics import PerformanceMetrics
from data.providers.yfinance_provider import YFinanceProvider
from data.storage.data_loader import DataLoader
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine

ticker ="ICICIBANK.NS"
provider = YFinanceProvider()
file_path = Path(f"data/raw/{ticker}.csv")
if file_path.exists():
    data = DataLoader.load_data(ticker)
else:
    data = provider.get_price_data(ticker)
    DataLoader.save_data(ticker, data)

strategy = STRATEGY_REGISTRY["rsi"]()
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