from typing import Tuple

import numpy as np


class ParametricInterpolate:
    def __init__(self, resolution=0.01):
        self.parameters = np.arange(0, 1 + resolution, resolution)

    def interpolate(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        '''
        Returns an parametric interpolated curve using the points
        :param x: list of x coordinates
        :param y: list of y coordinates
        :return: curve
        '''
        pass
