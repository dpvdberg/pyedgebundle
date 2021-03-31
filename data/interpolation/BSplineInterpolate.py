from typing import Tuple

from scipy import interpolate
from scipy.interpolate import KroghInterpolator

from data.interpolation.ParametricInterpolate import ParametricInterpolate
import numpy as np


class BSplineInterpolate(ParametricInterpolate):
    def __init__(self, resolution=0.01, smoothing=0, max_degree=3):
        super().__init__(resolution)
        self.max_degree = max_degree
        self.smoothing = smoothing

    def interpolate(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        numpoints_x = x.shape[0]
        numpoints_y = y.shape[0]
        assert numpoints_x == numpoints_y, "Size of x and y coordinate list must be equal"

        spline_degree = numpoints_x - 1 if numpoints_x <= self.max_degree else self.max_degree

        tck, u = interpolate.splprep([x, y], s=self.smoothing, k=spline_degree)
        out = interpolate.splev(self.parameters, tck)
        #
        # u = KroghInterpolator(x, y)
        # out = [u(i) for i in self.parameters]

        return out[0], out[1]
