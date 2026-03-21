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

        df = df.copy()

        # =========================
        # TIME-BASED SPLIT (RAW DATA)
        # =========================
        split = int(len(df) * 0.7)

        train_raw = df.iloc[:split]
        test_raw  = df.iloc[split:]

        # =========================
        # FEATURE ENGINEERING (SEPARATE)
        # =========================
        train = FeatureEngineer.create_features(train_raw)
        test  = FeatureEngineer.create_features(test_raw)

        # =========================
        # TRAIN DATA
        # =========================
        X_train = train[self.feature_cols]
        y_train = train["target"]

        # =========================
        # TEST DATA
        # =========================
        X_test = test[self.feature_cols]
        y_test = test["target"]

        # =========================
        # TRAIN MODEL
        # =========================
        self.model.train(X_train, y_train)

        # =========================
        # PREDICT PROBABILITIES
        # =========================
        probs = self.model.model.predict_proba(X_test)

        # Handle multi-class (-1, 0, 1)
        class_labels = self.model.model.classes_

        prob_df = pd.DataFrame(probs, columns=class_labels, index=test.index)

        # =========================
        # GENERATE SIGNALS (WITH HOLD ZONE)
        # =========================
        test = test.copy()
        test["signal"] = 0  # default HOLD

        # Buy when strong positive probability
        if 1 in prob_df.columns:
            test.loc[prob_df[1] > 0.55, "signal"] = 1

        # Sell when strong negative probability
        if -1 in prob_df.columns:
            test.loc[prob_df[-1] > 0.55, "signal"] = -1

        # =========================
        # METRICS (ON RAW PREDICTIONS)
        # =========================
        raw_predictions = self.model.model.predict(X_test)

        print("Accuracy:", accuracy_score(y_test, raw_predictions))
        print("Precision:", precision_score(y_test, raw_predictions, average="macro", zero_division=0))
        print("Recall:", recall_score(y_test, raw_predictions, average="macro", zero_division=0))

        return test.reset_index(drop=True)