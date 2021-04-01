import random
from unittest import TestCase
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm
from data.interpolation.BSplineInterpolate import BSplineInterpolate
from demo.demo import AirlineDemo, SmallDemo
from parse.GraphUtils import GraphUtils

G = nx.Graph()
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

nx.readwrite.write_graphml_xml(G, '../../examplegraphs/join.graphml', named_key_ids=True)

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
        np.random.seed(10)
        a = AntBundleAlgorithm(G, BSplineInterpolate(max_degree=2), 10, 4, True, 0.0001, 0.4, 0.0005, 5, 6)
        result = a.bundle()
        a.field.plot()
        result.plot()

        pos = {
            n: (d['x'], d['y']) for n, d in a.graph.nodes(data=True)
        }
        # Plot original network
        plt.axes().set_aspect('equal')
        nx.draw_networkx(a.graph, pos)
        plt.show()

        # Plot pheromone field
        a.field.plot()
        plt.show()

    def test_example2(self):
        random.seed(1)
        np.random.seed(1)
        a = AntBundleAlgorithm(G_pres, BSplineInterpolate(max_degree=3), 1000, 3, False, 0.97, 0.3, 0.0005, 5, 6)
        result = a.bundle()
        a.field.plot(cm='plasma')
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
        d = {}
        for node, data in g.nodes(data=True):
            d[node] = {'x': int(data["x"] * 0.7),
                       'y': int(data["y"]* 0.7)}
        nx.set_node_attributes(g, d)

        a = AntBundleAlgorithm(g, BSplineInterpolate(max_degree=3), 100, 4, False, 0.98, 0.4, 0.0005, 5, 6)
        a.bundle().plot()
        a.field.plot()

    def test_small_demo(self):
        random.seed(1)
        np.random.seed(1)
        g = SmallDemo().get_graph()
        a = AntBundleAlgorithm(g, BSplineInterpolate(max_degree=3), 1, 4, False, 0.98, 0.4, 0.0005, 5, 6)
        a.bundle().plot()
