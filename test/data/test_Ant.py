import math
from unittest import TestCase

import networkx as nx

from data.Ant import Ant
from data.PheromoneField import PheromoneField

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(1, 4)


class TestAnt(TestCase):
    def test_get_left_antenna(self):
        ant = Ant((0, 0), (-2, -2))

        self.assertEqual(ant.getLeftAntenna(), (1, 1))

        ant.updateDirection(math.pi / 2)

        self.assertEqual(ant.getLeftAntenna(), (-1, 1))

    def test_get_right_antenna(self):
        ant = Ant((0, 0), (-2, -2))

        self.assertEqual(ant.getRightAntenna(), (1, -1))

        ant.updateDirection(math.pi / 2)

        self.assertEqual(ant.getRightAntenna(), (1, 1))

    def test_get_candidate_neighbours(self):
        ant = Ant((0, 0), (2, 2))
        field = PheromoneField((10, 10), G, True, 0.01, 0.1, 0.1, 2)
        neighbours = field.getCandidateNeighbours(ant)

        self.assertEqual(set(neighbours), {(0, 1), (1, 1), (1, 0)})

    def test_get_candidate_neighbours2(self):
        ant = Ant((2, 2), (0, 0))
        field = PheromoneField((10, 10), G, True, 0.01, 0.1, 0.1, 2)
        neighbours = field.getCandidateNeighbours(ant)

        self.assertEqual(set(neighbours), {(3, 1), (2, 1)})

    def test_get_candidate_neighbours3(self):
        ant = Ant((2, 2), (0, 0))
        ant.updateDirection(math.pi / 4)

        field = PheromoneField((10, 10), G, True, 0.01, 0.1, 0.1, 2)
        neighbours = field.getCandidateNeighbours(ant)

        self.assertEqual(set(neighbours), {(1, 3), (3, 1)})
