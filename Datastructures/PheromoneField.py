from typing import Tuple

from networkx import DiGraph

from Datastructures.Ant import Ant


class PheromoneField:

    def __init__(self, pixels, graph: DiGraph):
        self.field = [[0 for col in range(pixels)] for row in range(pixels)]
        for node in graph.nodes:
            # TODO: set pixel to pheromone value
            pass

        self.g = graph

    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self, r):
        for run in r:
            ants = []
            for e in self.g.edges:
                ant = self.initializeEdge(e)
                ants.append(ant)
                while not ant.reachedGoal():
                    nextCell = self.antWalk(ant)
                    ant.addToPath(nextCell)
            for ant in ants:
                self.updateField(ant.path)
            self.evaporate()

    # Return an ant that walks along the given edge
    def initializeEdge(self, edge) -> Ant:
        return Ant((self.g.nodes[edge[0]]['x'], self.g.nodes[edge[0]]['y']), (self.g.nodes[edge[1]]['x'], self.g.nodes[edge[1]]['y']))

    # Calculate the new direction for an individual ant
    def antWalk(self, ant) -> Tuple:
        pass

    # Update values of field using the given path
    def updateField(self, path):
        pass

    # Evaporate field values after a run
    def evaporate(self):
        pass
