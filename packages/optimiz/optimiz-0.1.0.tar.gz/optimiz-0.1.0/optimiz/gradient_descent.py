from .optimizer import Optimizier
import numpy as np
from .logger import get_logger

class GradientDescent(Optimizier):
    
    def __init__(self, learning_rate, iterations, tolerance) -> None:
        super().__init__(learning_rate, iterations, tolerance)
        self.logger = get_logger(self.__class__.__name__)


    def optimize(self ,X , y , initial_weights = None ):

        m , n = X.shape

        weights = initial_weights.copy()

        for i in range(self.iterations):
            gradient = self._compute_gradient(X , y, weights)
            updated_weights = weights - self.learning_rate * gradient
            weights = updated_weights
        
        return weights
    
    def _compute_cost(self , X , y , weights):
        m = len(y)
        predictions = X.dot(weights)
        return (1/(2*m)) * np.sum((predictions - y)**2)

    
    def _compute_gradient(self, X , y , weights):
        m = len(y)
        predictions = X.dot(weights)

        gradient = (1/m) * X.T.dot(predictions - y)
        return gradient