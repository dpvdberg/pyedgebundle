import math
import numpy as np
from unittest import TestCase

import networkx as nx

from data.PheromoneField import PheromoneField

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(1, 4)


class TestPheromoneField(TestCase):
    def test_build_field(self):
        self.fail()

    def test_ant_walk(self):
        self.fail()

    def test_update_field(self):
        test = PheromoneField((7, 7), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (3, x) for x in range(7)
        ]
        test.updateField(path)

        self.assertEqual(np.count_nonzero(test.field), 35)
        self.fail()

    def test_update_field_diag(self):
        test = PheromoneField((7, 7), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (x, x) for x in range(7)
        ]
        test.updateField(path)

        self.assertEqual(np.count_nonzero(test.field), 7 + 6 * 2 + 5 * 2)

    def test_get_path_length(self):
        self.fail()

    def test_evaporate(self):
        self.fail()

    def test_random_directional_change(self):
        test = PheromoneField((10, 10), G, True, 0.01, 0.1, 0.1, 2)
        for i in range(0, 100):
            self.assertTrue(-math.pi <= test.randomDirectionalChange() <= math.pi)

    def test_pheromone_based_direction(self):
        self.fail()
