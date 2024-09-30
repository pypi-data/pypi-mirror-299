import numpy as np
from .gradient_descent import GradientDescent

class LinearRegression:

    def __init__(self, learning_rate = 0.01 , iterations = 1000 , tolerance = 1e-6) -> None:
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.tolerance = tolerance
        self.weights = None
        self.optimizer = GradientDescent(learning_rate , iterations , tolerance)
    
    def fit(self, X , y):

        X_with_bias = np.c_[np.ones((X.shape[0] , 1)) , X]

        initial_weights = np.zeros(X_with_bias.shape[1])

        self.weights = self.optimizer.optimize(X_with_bias , y , initial_weights)
    
    def predict(self , X):

        if self.weights is None:
            raise ValueError("Model has not been trained. Call fit() first.")
        X_with_bias = np.c_[np.ones((X.shape[0] , 1 )) , X]
        return X_with_bias.dot(self.weights)
    
 