from algorithms.BundleAlgorithm import BundleAlgorithm
from Datastructures.PheromoneField import PheromoneField


class AntBundleAlgorithm(BundleAlgorithm):

    def __init__(self, graph):
        self.graph = graph
        self.field = PheromoneField

    # Bundle edges in the given graph and return a BundledGraph object
    def bundle(self, graph):
        pass
