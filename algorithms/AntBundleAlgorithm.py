from algorithms.BundleAlgorithm import BundleAlgorithm
from data.PheromoneField import PheromoneField
from networkx import Graph


# Edge bundling algorithm that performs edge bundling based on ant colony optimization
class AntBundleAlgorithm(BundleAlgorithm):

    def __init__(self, graph: Graph, runs, pixels):
        self.graph = graph
        self.field = PheromoneField(pixels, graph)
        self.r = runs

    # Bundle edges in the given graph and return a BundledGraph object
    def bundle(self, graph):
        self.field.buildField(self.r)
        return self.createCurves(self.field)

    # Create and return a BundledGraph with curved edges based on the given Pheromone field
    def createCurves(self, field):
        pass
