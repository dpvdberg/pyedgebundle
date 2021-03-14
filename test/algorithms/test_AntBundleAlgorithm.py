from unittest import TestCase
import networkx as nx

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm

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

class TestAntBundleAlgorithm(TestCase):
    def test_create_curves(self):
        a = AntBundleAlgorithm(G, 2, 2, False, 0.1, 0.1, 0.01, 2)
        a.bundle()