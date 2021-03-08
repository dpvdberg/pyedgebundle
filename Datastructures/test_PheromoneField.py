import math
from unittest import TestCase

import networkx as nx

from Datastructures.PheromoneField import PheromoneField

G = nx.DiGraph()
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(1,4)

class TestPheromoneField(TestCase):
    def test_build_field(self):
        self.fail()

    def test_ant_walk(self):
        self.fail()

    def test_update_field(self):
        self.fail()

    def test_get_path_length(self):
        self.fail()

    def test_evaporate(self):
        self.fail()

    def test_random_directional_change(self):
        test = PheromoneField(10, G, True, 0.01, 0.1, 0.1, 2)
        for i in range(0,100):
            self.assertTrue(-math.pi <= test.randomDirectionalChange() <= math.pi)

    def test_pheromone_based_direction(self):
        self.fail()
