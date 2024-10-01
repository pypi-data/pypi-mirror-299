import math

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KDTree


class SmoothKNeighborsClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, n_neighbors=18, gamma=0.9):
        self.n_neighbors = n_neighbors
        self.gamma = gamma

    def fit(self, X, y):
        self.tree = KDTree(np.array(X))
        self.classes_ = np.array(sorted(set(y)))
        self.y = np.array(y)

    def predict(self, X):
        predictions = []
        distances, closest = self.tree.query(np.array(X), k=self.n_neighbors)
        for x in range(len(X)):
            results = {}
            for i, c in enumerate(closest[x]):
                value = self.y[c]
                if value not in results:
                    results[value] = []
                results[value].append(distances[x][i])
            for key, value in results.items():
                results[key] = np.mean(value) * math.pow(self.gamma, len(value))
            predictions.append(min(results, key=results.get))
        return np.array(predictions)
