import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class BundledGraph:
    def __init__(self, graph: nx.Graph, curves: np.ndarray):
        self.curves = curves
        self.graph = graph

    def plot(self, fig=None, ax=None, show=True, edges=True):
        if fig is None and ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        elif fig is None:
            ax.cla()
        elif ax is None:
            raise Exception("Cannot pass figure without axes")

        ax.set_aspect('equal')

        pos = {
            n: (d['x'], d['y']) for n, d in self.graph.nodes(data=True)
        }

        nx.draw_networkx_nodes(self.graph, pos,
                               ax=ax,
                               node_size=100)

        if edges:
            for curve in self.curves:
                ax.plot(curve[0], curve[1], 'k-', linewidth=1)

        if show:
            plt.show()
