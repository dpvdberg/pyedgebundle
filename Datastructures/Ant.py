import math
from typing import List

import numpy


class Ant:

    def __init__(self, start, goal):
        self.location = start
        self.goal = goal
        self.direction = 0
        self.path = [start]

    def reachedGoal(self):
        return self.location == self.goal

    def addToPath(self, next):
        self.path.append(next)

    def updateDirection(self, newDirec):
        self.direction = self.direction + newDirec

    def getLeftAntenna(self):
        return self.calcPixel(self.direction + math.pi/4)

    def getRightAntenna(self):
        return self.calcPixel(self.direction - math.pi/4)

    def getCandidateNeighbours(self) -> List:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbours.append((self.location[0] + i, self.location[1] + j))
        neighbours.remove(self.location)

        # Only use neighbours that have not been visited before
        nvisited = [x for x in neighbours if x not in self.path]
        if not nvisited:
            return neighbours

        # Only consider neighbours that are not further away from the goal
        angleEnd = self.calcAngle(self.goal)
        # TODO: optimize using modulo operation instead of arctan
        nborder = [x for x in nvisited if -math.pi * 3 / 4 < math.atan2(math.sin(angleEnd - self.calcAngle(x)), math.cos(angleEnd - self.calcAngle(x))) < math.pi * 3 / 4 ]
        if not nborder:
            return nvisited

        # Only consider neighbours that make sharp turns w.r.t. our current position
        nfinal = [x for x in nborder if -math.pi / 2 <= math.atan2(math.sin(self.direction - self.calcAngle(x)), math.cos(self.direction - self.calcAngle(x))) <= math.pi / 2]
        if not nfinal:
            return nborder
        return nfinal

    def takeStep(self):
        newLoc = self.calcPixel(self.direction)
        self.location = newLoc
        self.addToPath(newLoc)

    def calcPixel(self, direction):
        return (round(self.location[0] + math.cos(direction)),
                     round(self.location[1] + math.sin(direction)))

    def calcAngle(self, goal):
        return math.atan2(goal[1] - self.location[1], goal[0] - self.location[0])