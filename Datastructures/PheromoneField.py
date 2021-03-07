import math
from typing import Tuple

import numpy
from networkx import DiGraph
import random

from Datastructures.Ant import Ant


class PheromoneField:

    def __init__(self, pixels, graph: DiGraph, decreaseByConstant, decreaseValue, p, threshold):
        self.field = numpy.zeros(pixels)
        for node in graph.nodes:
            # TODO: set pixel to pheromone value
            pass

        self.g = graph
        self.decreaseByConstant = decreaseByConstant
        self.decreaseValue = decreaseValue
        self.p = p
        self.t = threshold

    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self, r, p):
        for run in r:
            ants = []
            for e in self.g.edges:
                ant = self.initializeEdge(e)
                ants.append(ant)
                while not ant.reachedGoal():
                    self.antWalk(ant)
            for ant in ants:
                self.updateField(ant.path)
            self.evaporate()

    # Return an ant that walks along the given edge
    def initializeEdge(self, edge) -> Ant:
        return Ant((self.g.nodes[edge[0]]['x'], self.g.nodes[edge[0]]['y']), (self.g.nodes[edge[1]]['x'], self.g.nodes[edge[1]]['y']))

    # Calculate the new direction for an individual ant
    def antWalk(self, ant: Ant):
        neighbours = ant.getCandidateNeighbours()
        if len(neighbours) == 1:
            newDirec = neighbours[0]
        else:
            rand = numpy.random.uniform(0, 1)
            if rand < self.p:
                newDirec = self.randomDirectionalChange()
            else:
                newDirec = self.pheromoneBasedDirection(neighbours, ant)
        ant.updateDirection(newDirec)
        ant.takeStep()

    # Update values of field using the given path
    def updateField(self, path):
        pass

    # Evaporate field values after a run
    def evaporate(self):
        if (self.decreaseByConstant):
            self.field - self.decreaseValue
        else:
            self.field * self.decreaseValue

    # Take random new directional change
    def randomDirectionalChange(self):
        return numpy.random.normal(0, numpy.pi/6)

    # Calculate directional change based on neighbours
    def pheromoneBasedDirection(self, neighbours, ant) -> float:
        l = ant.getLeftAntenna()
        r = ant.getRightAntenna()
        if l in neighbours and r in neighbours:
            fLeft = self.field[l]
            fRight = self.field[r]
            if fLeft == 0 and fRight == 0:
                if self.field[ant.location] > 0:
                    return 0
                else:
                    return numpy.random.normal(0, math.pi/6)
            elif math.fabs(fLeft - fRight) < self.t:
                return numpy.random.normal(0, math.pi/6)
            else:
                rand = numpy.random.uniform(0, fLeft**4 + fRight**4)
                return (-1 if rand < fLeft**4 else 1) * math.pi/4
        elif l in neighbours and not r in neighbours:
            return math.pi/4
        elif not l in neighbours and r in neighbours:
            return -math.pi/4
        else:
            return numpy.random.normal(0, math.pi/6)
