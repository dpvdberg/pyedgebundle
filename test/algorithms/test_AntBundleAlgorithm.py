import random
from unittest import TestCase
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

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

G_pres = nx.DiGraph()
G_pres.add_nodes_from([
    (1, {"x": 20, "y": 100}),
    (2, {"x": 150, "y": 80}),
    (3, {"x": 140, "y": 140}),
    (4, {"x": 50, "y": 20}),
    (5, {"x": 190, "y": 130})
])
G_pres.add_edge(1, 2)
G_pres.add_edge(1, 3)
G_pres.add_edge(1, 4)
G_pres.add_edge(4, 3)
G_pres.add_edge(2, 3)
G_pres.add_edge(3, 5)

class TestAntBundleAlgorithm(TestCase):
    def test_example(self):
        random.seed(1)
        np.random.seed(1)
        a = AntBundleAlgorithm(G, BSplineInterpolate(max_degree=2), 30, 4, True, 0.0001, 0.4, 0.0005, 5)
        result = a.bundle()
        a.field.plot()
        result.plot()

        pos = {
            n: (d['x'], d['y']) for n, d in a.graph.nodes(data=True)
        }
        # Plot original network
        nx.draw_networkx(a.graph, pos)
        plt.show()

        # Plot pheromone field
        a.field.plot()
        plt.show()

    def test_example2(self):
        random.seed(1)
        np.random.seed(1)
        a = AntBundleAlgorithm(G_pres, BSplineInterpolate(max_degree=2), 50, 20, True, 0.0015, 0.4, 0.0005, 10)
        result = a.bundle()
        a.field.plot()
        result.plot()

        pos = {
            n: (d['x'], d['y']) for n, d in a.graph.nodes(data=True)
        }
        # Plot original network
        nx.draw_networkx(a.graph, pos)
        plt.show()

        # Plot pheromone field
        a.field.plot()
        plt.show()

    def test_demo(self):
        g = AirlineDemo().get_graph()
        a = AntBundleAlgorithm(g, BSplineInterpolate(max_degree=3), 1, 4, True, 0.0015, 0.4, 0.0005, 5)
        a.bundle().plot()
