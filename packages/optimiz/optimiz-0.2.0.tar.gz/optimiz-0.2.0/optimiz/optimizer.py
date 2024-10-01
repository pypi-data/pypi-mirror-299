import numpy as np


class Optimizier:

    def __init__(self , learning_rate , iterations , tolerance) -> None:
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.tolerance = tolerance

    def optimize(self):
        return NotImplementedError("Subclasses should implement this method.")
    
    