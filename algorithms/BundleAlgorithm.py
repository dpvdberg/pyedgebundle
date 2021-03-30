from data import BundledGraph

# An algorithm that performs edge bundling on a given graph
from data.interpolation.ParametricInterpolate import ParametricInterpolate


class BundleAlgorithm:
    def __init__(self, interpolation: ParametricInterpolate):
        self.interpolation = interpolation

    def bundle(self) -> BundledGraph:
        """"Apply edge bundling to the given graph"""
        pass
