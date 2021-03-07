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
        return (round(self.location[0] + math.cos(self.direction + math.pi/4)),
                round(self.location[1] + math.sin(self.direction + math.pi/4)))

    def getRightAntenna(self):
        return (round(self.location[0] + math.cos(self.direction + math.pi / 4)),
                round(self.location[1] + math.sin(self.direction + math.pi / 4)))

    def getCandidateNeighbours(self) -> List:
        pass

    def takeStep(self):
        newLoc = (round(self.location[0] + math.cos(self.direction)),
                     round(self.location[1] + math.sin(self.direction)))
        self.location = newLoc
        self.addToPath(newLoc)