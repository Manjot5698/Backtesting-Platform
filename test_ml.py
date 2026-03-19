import pandas as pd
from ml.pipeline import MLPipeline
from engine.backtest_engine import BacktestEngine
from analytics.performance_metrics import PerformanceMetrics


# Load data
df = pd.read_csv("data/raw/ICICIBANK.NS.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Run ML pipeline
pipeline = MLPipeline()
result = pipeline.run(df)

# Show ML output
print("\nML Output:")
print(result.tail())

# Show prediction distribution
print("\nPrediction Distribution:")
print(result["signal"].value_counts())

# Run backtest
engine = BacktestEngine(result)
backtest_result = engine.run()

# Show backtest output
print("\nBacktest Output:")
print(backtest_result.tail())

# Performance metrics
print("\nPerformance Metrics")
print("Total Return:", PerformanceMetrics.total_return(backtest_result))
print("Max Drawdown:", PerformanceMetrics.max_drawdown(backtest_result))
print("Sharpe Ratio:", PerformanceMetrics.sharpe_ratio(backtest_result))