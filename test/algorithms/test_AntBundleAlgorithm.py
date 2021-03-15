import random
from unittest import TestCase
import networkx as nx

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm
from data.interpolation.BSplineInterpolate import BSplineInterpolate
from demo.demo import AirlineDemo

G = nx.DiGraph()
G.add_nodes_from([
    (1, {"x": 0, "y": 0}),
    (2, {"x": 0, "y": 50}),
    (3, {"x": 0, "y": 100}),
    (4, {"x": 0, "y": 150}),
    (5, {"x": 0, "y": 200}),
    (6, {"x": 700, "y": 100}),
])
for i in range(1, 6):
    G.add_edge(i, 6)


class TestAntBundleAlgorithm(TestCase):
    def test_example(self):
        random.seed(1)
        a = AntBundleAlgorithm(G, BSplineInterpolate(max_degree=3), 100, 4, True, 0.0015, 0.4, 0.0005, 5)
        a.bundle().plot()

    def test_demo(self):
        g = AirlineDemo().get_graph()
        a = AntBundleAlgorithm(g, BSplineInterpolate(max_degree=4), 10, 3, False, 0.1, 0.1, 0.01, 2)
        a.bundle().plot()
