class PheromoneField:

    def __init(self, nodes):
        self.field = float[nodes][nodes]

    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self):
        pass

    # Let all ants in the network take a single step to their goal
    def step(self):
        pass

    # Calculate the new direction for an individual ant
    def antWalk(self):
        pass
