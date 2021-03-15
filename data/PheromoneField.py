import math
from typing import Tuple

import numpy as np
from networkx import DiGraph
from matplotlib import pyplot as plt
import random

from data.Ant import Ant


# euclidean distance between two cells
def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


class PheromoneField:

    def __init__(self, pixels: Tuple[int, int, int], graph: DiGraph, decreaseByConstant, decreaseValue, p, threshold,
                 maxUpdateDistance):
        self.field = np.zeros(pixels)
        self.g = graph
        self.decreaseByConstant = decreaseByConstant
        self.decreaseValue = decreaseValue
        self.p = p
        self.t = threshold
        self.maxUpdateDistance = maxUpdateDistance

        self.columns, self.rows, self.numtypes = self.field.shape

    def get_rectangle(self):
        # xmin, ymin, xmax, ymax
        return 0, 0, self.columns - 1, self.rows - 1

    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self, r):
        for run in range(r):
            print("run: ", run)
            ants = []
            for e in self.g.edges:
                # For each edge, create an ant and let it walk until it reaches its goal
                ant = self.initializeEdge(e)
                ants.append(ant)
                while not ant.reachedGoal():
                    self.antWalk(ant)
            # Update the field with the new found paths
            for ant in ants:
                self.updateField(ant.path, ant.start_index, ant.end_index)
                # print(self.field.sum(axis=2))
                # self.plot()
            # Evaporate value of all fields such that bad paths will eventually disappear
            self.evaporate()

    # Return an ant that walks along the given edge
    def initializeEdge(self, edge) -> Ant:
        return Ant((self.g.nodes[edge[0]]['x'], self.g.nodes[edge[0]]['y']),
                   (self.g.nodes[edge[1]]['x'], self.g.nodes[edge[1]]['y']), edge[0], edge[1])

    # Calculate the new direction for an individual ant
    def antWalk(self, ant: Ant):
        neighbours = self.getCandidateNeighbours(ant)
        # If only one neighbour is valid, walk to that pixel
        if len(neighbours) == 1:
            newDirec = ant.calcAngle(neighbours[0]) - ant.direction
        elif ant.goal in neighbours:
            newDirec = ant.calcAngle(ant.goal) - ant.direction
        else:
            newDirec = None
            while newDirec is None or not self.is_valid_location(*ant.calcPixel(ant.direction + newDirec)):
                # With chance p we either get a random directional change, or a pheromone based directional change
                rand = np.random.uniform(0, 1)
                if rand < self.p:
                    newDirec = self.randomDirectionalChange()
                else:
                    newDirec = self.pheromoneBasedDirection(neighbours, ant)

        # Update the ant's new direction
        ant.updateDirection(newDirec)
        # Let the ant take a step
        ant.takeStep()

    def is_valid_location(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    # Update values of field using the given path
    def updateField(self, path, start_index, end_index):

        def visitNeighbors(cell, original_cell=None, visited_nodes=None):
            if original_cell is None:
                original_cell = cell

            if visited_nodes is None:
                visited_nodes = {}

            cx, cy = cell

            # loop over direct neighbors
            for x in range(cx - 1, cx + 2):
                for y in range(cy - 1, cy + 2):
                    if not self.is_valid_location(x, y):
                        # out of range
                        continue

                    c = (x, y)
                    if c not in visited_nodes:
                        # euclidean distance
                        d = euclidean(original_cell, c)
                        if d <= self.maxUpdateDistance:
                            visited_nodes[c] = d
                            visitNeighbors(c, original_cell, visited_nodes)

            return visited_nodes

        # A dictionary mapping a cell to the minimum distance to the path
        min_distance_dict = {}

        for cell in path:
            neighbors = visitNeighbors(cell)
            min_distance_dict = {k: min(i for i in (min_distance_dict.get(k), neighbors.get(k)) if i is not None)
                                 for k in min_distance_dict.keys() | neighbors}

        # update field using dict
        # TODO: collect min_distance_dict for all paths and then compute average (or KDE?) for overlapping cells
        path_constant = self.getPathUpdateConstant(path)

        for cell, distance in min_distance_dict.items():
            self.field[cell][start_index] = self.field[cell][start_index] \
                                            + path_constant * math.exp(
                -distance ** 2 / (2 * (self.maxUpdateDistance / 3) ** 2))
            self.field[cell][end_index] = self.field[cell][end_index] \
                                          + path_constant * math.exp(
                -distance ** 2 / (2 * (self.maxUpdateDistance / 3) ** 2))

    def getPathUpdateConstant(self, path):
        return (euclidean(path[0], path[-1]) / self.getPathLength(path)) ** 8

    def getPathLength(self, path):
        s = 0
        for i in range(len(path) - 1):
            s = s + euclidean(path[i], path[i + 1])
        return s

    # Evaporate field values after a run
    def evaporate(self):
        # Depending on whether the user choose a constant value decrease, or multiplying by a factor between (0, 1)
        if (self.decreaseByConstant):
            self.field = self.field - self.decreaseValue
            self.field[self.field < 0] = 0
        else:
            self.field = self.field * self.decreaseValue

    # Take random new directional change
    def randomDirectionalChange(self) -> float:
        return np.random.normal(0, math.pi / 6)

    # Calculate directional change based on neighbours
    def pheromoneBasedDirection(self, neighbours, ant) -> float:
        # Calculate left and right antenna pixels and their values
        l = ant.getLeftAntenna()
        r = ant.getRightAntenna()

        fLeft, fRight = 0, 0

        if l in neighbours:
            fLeft = sum(self.field[l])

        if r in neighbours:
            fRight = sum(self.field[r])

        if l in neighbours and r in neighbours:
            if fLeft == 0 and fRight == 0:
                if sum(self.field[ant.location]) > 0:
                    # If both are 'bad' neighbours and we are on a path with a high pheromone value, continue walking
                    return 0
                else:
                    # If both are 'bad' neighbours and we are on a 'bad' path, take a random directional change
                    return np.random.normal(0, math.pi / 6)

            # If both antenna are our neighbours but the difference in their values is too small, random change
            elif math.fabs(fLeft - fRight) < self.t:
                return np.random.normal(0, math.pi / 6)
            else:
                # Else, both antenna are neighbours but their value difference is large enough
                rand = np.random.uniform(0, fLeft ** 4 + fRight ** 4)
                # Go left or right, depending on the pheromone values of l and r
                return (-1 if rand < fLeft ** 4 else 1) * math.pi / 4

        # If only l is a neighbour, go left
        elif l in neighbours and not r in neighbours:
            return math.pi / 4

        # If only r is a neighbour, go right
        elif not l in neighbours and r in neighbours:
            return -math.pi / 4

        # If neither are neighbours, pick a random directional change
        else:
            return np.random.normal(0, math.pi / 6)

    def getCandidateNeighbours(self, ant) -> list:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid_location(ant.location[0] + i, ant.location[1] + j) and not (i == 0 and j == 0):
                    neighbours.append((ant.location[0] + i, ant.location[1] + j))

        # Only use neighbours that have not been visited before
        nvisited = [x for x in neighbours if x not in ant.path]
        if not nvisited:
            return neighbours

        # Only consider neighbours that are not further away from the goal
        angleEnd = ant.calcAngle(ant.goal)
        # TODO: optimize using modulo operation instead of arctan
        nborder = [x for x in nvisited if -math.pi * 3 / 4 < math.atan2(math.sin(angleEnd - ant.calcAngle(x)), math.cos(
            angleEnd - ant.calcAngle(x))) < math.pi * 3 / 4]
        if not nborder:
            return nvisited

        # Only consider neighbours that make sharp turns w.r.t. our current position
        nfinal = [x for x in nborder if -math.pi / 2 <= math.atan2(math.sin(ant.direction - ant.calcAngle(x)), math.cos(
            ant.direction - ant.calcAngle(x))) <= math.pi / 2]
        if not nfinal:
            return nborder
        return nfinal

    def plot(self, cm='viridis'):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        plt.imshow(self.field.sum(axis=-1).T, interpolation='nearest', cmap=plt.cm.get_cmap(cm), origin='lower')
        plt.colorbar()
        plt.show()
