import pandas as pd
import numpy as np

from ml.features import FeatureEngineer
from ml.model import MLModel

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class MLPipeline:

    def __init__(self):
        self.model = MLModel()

        self.feature_cols = [
            "return", "momentum_5", "momentum_10",
            "sma_10", "sma_20", "sma_50",
            "ema_12", "ema_26",
            "volatility_10", "volatility_20",
            "macd", "signal_line", "macd_histogram",
            "RSI",
            "bb_position",
            "atr",
            "price_position"
        ]

    def run(self, df: pd.DataFrame):
        """Run ML pipeline: feature engineering, training, prediction"""

        df = df.copy()

        # =========================
        # TIME-BASED SPLIT (RAW DATA)
        # =========================
        split = int(len(df) * 0.7)

        train_raw = df.iloc[:split]
        test_raw = df.iloc[split:]

        # =========================
        # FEATURE ENGINEERING (SEPARATE)
        # =========================
        train = FeatureEngineer.create_features(train_raw)
        test = FeatureEngineer.create_features(test_raw)

        # =========================
        # PREPARE DATA
        # =========================
        # Filter feature_cols to only those that exist
        available_feature_cols = [col for col in self.feature_cols if col in train.columns]
        
        X_train = train[available_feature_cols]
        y_train = train["target"]

        # =========================
        # TEST DATA
        # =========================
        X_test = test[available_feature_cols]
        y_test = test["target"]

        # =========================
        # TRAIN MODEL
        # =========================
        self.model.train(X_train, y_train)

        # =========================
        # PREDICT PROBABILITIES
        # =========================
        probs = self.model.predict_proba(X_test)

        # Handle multi-class (-1, 0, 1)
        class_labels = self.model.model.classes_

        prob_df = pd.DataFrame(probs, columns=class_labels, index=X_test.index)

        # =========================
        # GENERATE SIGNALS (WITH CONFIDENCE)
        # =========================
        test = test.copy()
        test["signal"] = 0  # default HOLD
        test["confidence"] = 0.0

        # Buy when strong positive probability (> 0.55)
        if 1 in prob_df.columns:
            buy_mask = prob_df[1] > 0.55
            test.loc[buy_mask, "signal"] = 1
            test.loc[buy_mask, "confidence"] = prob_df.loc[buy_mask, 1]

        # Sell when strong negative probability (> 0.55)
        if -1 in prob_df.columns:
            sell_mask = prob_df[-1] > 0.55
            test.loc[sell_mask, "signal"] = -1
            test.loc[sell_mask, "confidence"] = prob_df.loc[sell_mask, -1]

        # =========================
        # METRICS (ON RAW PREDICTIONS)
        # =========================
        raw_predictions = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, raw_predictions)
        precision = precision_score(y_test, raw_predictions, average="macro", zero_division=0)
        recall = recall_score(y_test, raw_predictions, average="macro", zero_division=0)
        f1 = f1_score(y_test, raw_predictions, average="macro", zero_division=0)

        print(f"Model Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")

        # Store metrics for later access
        self.metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }

        return test.reset_index(drop=True)