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