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

    def takeStep(self):
        newLoc = self.calcPixel(self.direction)
        self.location = newLoc
        self.addToPath(newLoc)

    def calcPixel(self, direction):
        return (round(self.location[0] + math.cos(direction)),
                     round(self.location[1] + math.sin(direction)))

    def calcAngle(self, goal):
        return math.atan2(goal[1] - self.location[1], goal[0] - self.location[0])