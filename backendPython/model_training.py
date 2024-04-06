from sklearn.ensemble import IsolationForest
from pyod.models.auto_encoder import AutoEncoder
from pyod.models.lof import LOF

class ModelTrainer:
    def __init__(self, models=None):
        if models is None:
            self.models = [
                IsolationForest(),
                AutoEncoder(hidden_neurons=[64, 32, 32, 64]),
                LOF()
            ]
        else:
            self.models = models

    def train_models(self, X_train, X_test):
        # Train and evaluate models
        for model in self.models:
            model.fit(X_train)
            train_scores = model.decision_function(X_train)
            test_scores = model.decision_function(X_test)
