import pandas as pd
from ml.pipeline import MLPipeline
from engine.backtest_engine import BacktestEngine


df = pd.read_csv("data/raw/ICICIBANK.NS.csv")
df["Date"] = pd.to_datetime(df["Date"])

pipeline = MLPipeline()

result = pipeline.run(df)

print(result.tail())
print("\nPrediction Distribution:")
print(pd.Series(result["signal"]).value_counts())
# run ML pipeline
result = pipeline.run(df)

# run backtest
engine = BacktestEngine(result)
backtest_result = engine.run()

print(backtest_result.tail())