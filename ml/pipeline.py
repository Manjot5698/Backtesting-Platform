import pandas as pd

from ml.features import FeatureEngineer
from ml.model import MLModel

from sklearn.metrics import accuracy_score, precision_score, recall_score


class MLPipeline:

    def __init__(self):
        self.model = MLModel()

        self.feature_cols = [
            "return", "momentum_5",
            "sma_10", "sma_20",
            "volatility_10", "RSI"
        ]

    def run(self, df: pd.DataFrame):

        df = FeatureEngineer.create_features(df)

        # Time-based split
        split = int(len(df) * 0.7)

        train = df.iloc[:split]
        test  = df.iloc[split:]

        X_train = train[self.feature_cols]
        y_train = train["target"]

        X_test = test[self.feature_cols]
        y_test = test["target"]

        # Train
        self.model.train(X_train, y_train)

        # Predict
        predictions = self.model.predict(X_test)

        # Metrics
        print("Accuracy:", accuracy_score(y_test, predictions))
        print("Precision:", precision_score(y_test, predictions))
        print("Recall:", recall_score(y_test, predictions))

        # Convert to signals
        test = test.copy()
        test["signal"] = predictions  # no pd.Series

        # convert to trading signal
        test["signal"] = test["signal"].map({1: 1, 0: -1})

        return test.reset_index(drop=True)