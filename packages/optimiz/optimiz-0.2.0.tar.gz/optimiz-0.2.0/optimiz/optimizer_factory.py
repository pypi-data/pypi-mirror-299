from .gradient_descent import GradientDescent
from .coordinate_descent import CoordinateDescent

class OptimizerFactory:

    @staticmethod
    def get_optimizer(optimizer_type , **kwargs):

        if optimizer_type == "gradient_descent":
            return GradientDescent(**kwargs)
        if optimizer_type == "coordinate_descent":
            return CoordinateDescent(**kwargs)
    