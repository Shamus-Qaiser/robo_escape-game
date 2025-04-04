import random
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score

def train_model(dataset, model_type):
    # Demo purpose - simulate different datasets
    if dataset == 'images':
        # Simulate image classification
        X = np.random.rand(100, 10)  # 100 samples, 10 features
        y = np.random.randint(0, 2, 100)  # Binary classification
        model = RandomForestClassifier()
        model.fit(X, y)
        accuracy = round(accuracy_score(y, model.predict(X)), 2)
    elif dataset == 'tabular':
        # Simulate tabular data regression
        X = np.random.rand(100, 5)
        y = np.random.rand(100)
        model = LinearRegression()
        model.fit(X, y)
        accuracy = round(model.score(X, y), 2)
    else:
        # Default random accuracy
        accuracy = round(random.uniform(0.7, 0.95), 2)
    
    return {
        "model_name": f"{model_type}_model_{random.randint(1000,9999)}",
        "accuracy": accuracy,
        "dataset": dataset,
        "status": "Training completed",
        "model_type": model_type
    }