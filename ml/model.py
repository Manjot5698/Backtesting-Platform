from sklearn.ensemble import RandomForestClassifier
import numpy as np

class MLModel:

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            class_weight="balanced"
        )
        self.is_trained = False
        
    def train(self, X, Y):
        """Train the model on features and targets"""
        self.model.fit(X, Y)
        self.is_trained = True
        
    def predict(self, X):
        """Predict class labels"""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Predict class probabilities"""
        return self.model.predict_proba(X)
    
    def get_confidence(self, X):
        """Get prediction confidence scores"""
        if not self.is_trained:
            return np.array([0.0] * len(X))
        proba = self.predict_proba(X)
        return np.max(proba, axis=1)
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        if not self.is_trained:
            return None
        return self.model.feature_importances_