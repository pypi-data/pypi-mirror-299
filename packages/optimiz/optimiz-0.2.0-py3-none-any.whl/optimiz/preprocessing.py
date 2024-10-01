import numpy as np

class Preprocessing:

    def __init__(self) -> None:
        self.mean = None
        self.std = None

    def scale(self , X):

        self.mean = np.mean(X , axis = 0)
        self.std = np.std(X , axis = 0)
        return (X - self.mean) / self.std
    