import numpy as np

def mse_loss(y_true , y_pred):

    mse = (1/2) * np.mean((y_true - y_pred)**2)
    return mse

def mse_gradient(X , y_true , y_pred):

    m = len(y_true)
    gradient = (1/m) * X.T.dot(y_pred - y_true)

    return gradient

def mse_partial_gradient(X , y , weights , j):
    m = len(y)
    return (1/ m) * np.sum((X @ weights - y) * X[: , j])
