import math
from unittest import TestCase

from data.Ant import Ant


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
        neighbours = ant.getCandidateNeighbours()

        self.assertEqual(set(neighbours), {(1, -1), (0, 1), (1, 1), (1, 0)})

    def test_get_candidate_neighbours2(self):
        ant = Ant((0, 0), (-2, -2))
        neighbours = ant.getCandidateNeighbours()

        self.assertEqual(set(neighbours), {(1, -1), (0, -1)})

    def test_get_candidate_neighbours3(self):
        ant = Ant((0, 0), (-2, -2))
        ant.updateDirection(math.pi / 4)
        neighbours = ant.getCandidateNeighbours()

        self.assertEqual(set(neighbours), {(-1, 1), (1, -1)})
