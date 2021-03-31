import os
import pathlib

import networkx as nx
from matplotlib import pyplot as plt

from parse.GraphUtils import GraphUtils


class EBDemo:
    def path(self) -> str:
        pass

    def sanitize(self, g: nx.DiGraph) -> nx.DiGraph:
        pass

    def get_graph(self) -> nx.DiGraph:
        g = nx.read_graphml(
            os.path.join(pathlib.Path(__file__).parent.parent.absolute(),
                         'examplegraphs',
                         self.path()
                         ))
        return self.sanitize(g)


class SmallDemo(EBDemo):
    def path(self):
        return 'small.graphml'

    def sanitize(self, g: nx.DiGraph) -> nx.DiGraph:
        g, _ = GraphUtils.sanitize(g)
        return g


class AirlineDemo(EBDemo):
    def path(self):
        return 'airlines.graphml'

    def sanitize(self, g):
        # ints for node labels
        return GraphUtils.sanitize(g)[0]


if __name__ == '__main__':
    g = AirlineDemo().get_graph()

    pos = {n: (d['x'], d['y']) for n, d in g.nodes.items()}
    nx.draw(g, pos, node_size=10)
    plt.show()
