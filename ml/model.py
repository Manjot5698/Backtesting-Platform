from sklearn.ensemble import RandomForestClassifier

class MLModel:

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators = 100,
            max_depth = 5,
            random_state = 42)
        
    def train(self,X,Y):
        self.model.fit(X,Y)

    def predict(self,X):
        return self.model.predict(X)