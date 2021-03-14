import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class BundledGraph:
    def __init__(self, graph: nx.Graph, curves: np.ndarray):
        self.curves = curves
        self.graph = graph

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')

        pos = {
            n: (d['x'], d['y']) for n, d in self.graph.nodes(data=True)
        }

        for curve in self.curves:
            plt.plot(curve[0], curve[1])

        nx.draw_networkx_nodes(self.graph, pos)
        plt.show()
