class PheromoneField:

    def __init__(self, nodes):
        self.field = [[0 for col in range(nodes)] for row in range(nodes)]

    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self, r):
        pass

    # Let all ants in the network take a single step to their goal
    def step(self):
        pass

    # Calculate the new direction for an individual ant
    def antWalk(self):
        pass

    def getField(self):
        return self.field
