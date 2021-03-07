class Ant:

    def __init__(self, start_x , start_y, goal_x, goal_y):
        self.location = (start_x, start_y)
        self.goal = (goal_x, goal_y)
        self.direction = 0
        self.path = []

    def reachedGoal(self):
        return self.location == self.goal

    def addToPath(self, next):
        self.path.append(next)