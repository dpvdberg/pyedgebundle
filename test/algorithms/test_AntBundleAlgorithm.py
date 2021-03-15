import random
from unittest import TestCase
import networkx as nx

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm
from data.interpolation.BSplineInterpolate import BSplineInterpolate
from demo.demo import AirlineDemo

G = nx.DiGraph()
G.add_nodes_from([
    (1, {"x": 200, "y": 200}),
    (2, {"x": 900, "y": 200}),
    (3, {"x": 600, "y": 600}),
    (4, {"x": 400, "y": 800})
])
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(1, 4)
G.add_edge(1, 3)


class TestAntBundleAlgorithm(TestCase):
    def test_example(self):
        random.seed(1)
        a = AntBundleAlgorithm(G, BSplineInterpolate(max_degree=4), 10, 4, True, 0.0015, 0.1, 0.0005, 5)
        a.bundle().plot()

    def test_demo(self):
        g = AirlineDemo().get_graph()
        a = AntBundleAlgorithm(g, BSplineInterpolate(max_degree=4), 10, 3, False, 0.1, 0.1, 0.01, 2)
        a.bundle().plot()
