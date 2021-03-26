import math
import random

import numpy as np
from unittest import TestCase

import networkx as nx

from data.Ant import Ant
from data.PheromoneField import PheromoneField

G = nx.DiGraph()
G.add_nodes_from([
    (1, {"x": 2, "y": 2}),
    (2, {"x": 9, "y": 2}),
    (3, {"x": 6, "y": 6}),
    (4, {"x": 4, "y": 8})
])
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(1, 4)
G.add_edge(1, 3)


class TestPheromoneField(TestCase):
    def test_presentation(self):
        random.seed(1)
        np.random.seed(1)
        G_pres = nx.DiGraph()
        G_pres.add_nodes_from([
            (1, {"x": 2, "y": 10}),
            (2, {"x": 15, "y": 8}),
            (3, {"x": 14, "y": 14}),
            (4, {"x": 5, "y": 2}),
            (5, {"x": 19, "y": 13})
        ])
        G_pres.add_edge(1, 2)
        G_pres.add_edge(1, 3)
        G_pres.add_edge(1, 4)
        G_pres.add_edge(4, 3)
        G_pres.add_edge(2, 3)
        G_pres.add_edge(3, 5)

        test = PheromoneField((20, 20, 6), G_pres,  True, 0, 0.4, 0.000005, 3)
        test.buildField(10)
        test.plot()

        self.assertEqual(0, 0)

    def test_build_field(self):
        random.seed(1)
        np.random.seed(2)
        test = PheromoneField((10, 10, 5), G, True, 0.0015, 0.4, 0.0005, 3)
        test.buildField(5)
        test.plot()

        self.assertEqual(0, 0)

    def test_update_field(self):
        test = PheromoneField((7, 7, 5), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (3, x) for x in range(7)
        ]
        test.field += test.updateField(path, 0, 3)

        self.assertEqual(np.count_nonzero(test.field), 35 * 2)
        self.assertEqual(list(test.field[3][0]), [1, 0, 0, 1, 0])

    def test_update_field_diag(self):
        test = PheromoneField((7, 7, 5), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (x, x) for x in range(7)
        ]
        test.field += test.updateField(path, 0, 0)

        test.plot()

        self.assertEqual(np.count_nonzero(test.field), 7 + 6 * 2 + 5 * 2)

    def test_update_field_corner(self):
        test = PheromoneField((7, 7, 5), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (3, 0), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (6, 3)
        ]
        test.field += test.updateField(path, 0, 0)

        test.plot()

        self.assertEqual(np.count_nonzero(test.field), 7 + 6 * 2 + 5 * 2)

    def test_update_field_vee(self):
        test = PheromoneField((7, 7, 5), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (x, x) for x in range(4)
        ]
        path.extend([
            (x, 6 - x) for x in range(4, 7)
        ])
        test.field += test.updateField(path, 0, 0)

        test.plot()

        self.assertEqual(np.count_nonzero(test.field), 7 * 4 + 1)

    def test_random_directional_change(self):
        test = PheromoneField((10, 10, 5), G, True, 0.01, 0.1, 0.1, 2)
        for i in range(0, 100):
            self.assertTrue(-math.pi <= test.randomDirectionalChange() <= math.pi)

    def test_pheromone_based_direction(self):
        test = PheromoneField((10, 10, 5), G, True, 0.01, 0.1, 0.1, 2)
        ant = Ant((1, 1), (8, 8), 0, 0)

    def test_plot(self):
        test = PheromoneField((7, 7, 5), G, True, 0.01, 0.1, 0.1, 2)
        path = [
            (x, x) for x in range(7)
        ]
        test.updateField(path, 0, 0)

        # test.plot()
