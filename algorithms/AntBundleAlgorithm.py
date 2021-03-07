from algorithms.BundleAlgorithm import BundleAlgorithm
from Datastructures.PheromoneField import PheromoneField
from networkx import Graph

# Edge bundling algorithm that performs edge bundling based on ant colony optimization
class AntBundleAlgorithm(BundleAlgorithm):

    def __init__(self, graph: Graph, runs):
        self.graph = graph
        self.field = PheromoneField(graph.number_of_nodes())
        self.r = runs

    # Bundle edges in the given graph and return a BundledGraph object
    def bundle(self, graph):
        self.field.buildField(self.r)
        return self.createCurves(self.field.getField())

    # Create and return a BundledGraph with curved edges based on the given Pheromone field
    def createCurves(self, field):
        pass
