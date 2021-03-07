import math
from typing import Tuple

import numpy as np
from networkx import DiGraph

from Datastructures.Ant import Ant


# euclidean distance between two cells
def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


class PheromoneField:

    def __init__(self, pixels, graph: DiGraph, decreaseByConstant, decreaseValue, maxUpdateDistance):
        self.field = np.zeros(pixels)
        for node in graph.nodes:
            # TODO: set pixel to pheromone value
            pass

        self.g = graph
        self.decreaseByConstant = decreaseByConstant
        self.decreaseValue = decreaseValue
        self.maxUpdateDistance = maxUpdateDistance

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
        return Ant((self.g.nodes[edge[0]]['x'], self.g.nodes[edge[0]]['y']),
                   (self.g.nodes[edge[1]]['x'], self.g.nodes[edge[1]]['y']))

    # Calculate the new direction for an individual ant
    def antWalk(self, ant) -> Tuple:
        pass

    # Update values of field using the given path
    def updateField(self, path):

        def visitNeighbors(cell, visited_nodes=None):
            if visited_nodes is None:
                visited_nodes = {}

            cx, cy = cell

            # loop over direct neighbors
            for x in range(cx - 1, cx + 1):
                for y in range(cx - 1, cx + 1):
                    c = (x, y)
                    if c not in visited_nodes:
                        # euclidean distance
                        d = euclidean(cell, c)
                        if d <= self.maxUpdateDistance:
                            visited_nodes[c] = d
                            visitNeighbors(c, visited_nodes)

            return visited_nodes

        # A dictionary mapping a cell to the minimum distance to the path
        min_distance_dict = {}

        for cell in path:
            neighbors = visitNeighbors(cell)
            min_distance_dict = {k: min(i for i in (min_distance_dict.get(k), neighbors.get(k)) if i)
                                 for k in min_distance_dict.keys() | neighbors}

        # update field using dict
        # TODO: collect min_distance_dict for all paths and then compute average (or KDE?) for overlapping cells
        path_constant = self.getPathUpdateConstant(path)

        for cell, distance in min_distance_dict.items():
            self.field[cell] = self.field[cell] \
                               + path_constant * math.exp(-distance ** 2 / (2 * (self.maxUpdateDistance / 3) ** 2))

    def getPathUpdateConstant(self, path):
        return (euclidean(path[0], path[-1]) / self.getPathLength(path)) ** 8

    def getPathLength(self, path):
        s = 0
        for i in range(len(path) - 1):
            s = s + euclidean(path[i], path[i + 1])
        return s

    # Evaporate field values after a run
    def evaporate(self):
        if (self.decreaseByConstant):
            self.field - self.decreaseValue
        else:
            self.field * self.decreaseValue
