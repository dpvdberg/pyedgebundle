import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class BundledGraph:
    def __init__(self, graph: nx.Graph, curves: np.ndarray):
        self.curves = curves
        self.graph = graph

    def plot(self, fig=None, ax=None, show=True):
        if fig is None:
            fig = plt.figure()
        if ax is None:
            ax = fig.add_subplot(1, 1, 1)
        else:
            ax.cla()

        ax.set_aspect('equal')

        pos = {
            n: (d['x'], d['y']) for n, d in self.graph.nodes(data=True)
        }

        for curve in self.curves:
            ax.plot(curve[0], curve[1])

        nx.draw_networkx_nodes(self.graph, pos, ax=ax)

        if show:
            plt.show()
