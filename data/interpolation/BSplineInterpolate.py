from scipy import interpolate
from data.interpolation.ParametricInterpolate import ParametricInterpolate
import numpy as np


class BSplineInterpolate(ParametricInterpolate):
    def __init__(self, resolution=0.01, smoothing=0):
        super().__init__(resolution)
        self.smoothing = smoothing

    def interpolate(self, points: np.ndarray) -> np.ndarray:
        x, y = [m.flatten() for m in np.split(points, 2, axis=1)]
        tck, u = interpolate.splprep([x, y], s=self.smoothing)
        out = interpolate.splev(self.parameters, tck)
        return out.T
