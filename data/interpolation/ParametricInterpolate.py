import numpy as np


class ParametricInterpolate:
    def __init__(self, resolution=0.01):
        self.parameters = np.arange(0, 1 + resolution, resolution)

    def interpolate(self, points: np.ndarray) -> np.ndarray:
        '''
        Returns an parametric interpolated curve using the points
        :param points: Points to use during interpolation
        :return: curve
        '''
        pass
