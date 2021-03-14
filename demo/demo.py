import os
import pathlib
from enum import Enum
import networkx as nx
from matplotlib import pyplot as plt


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


class AirlineDemo(EBDemo):
    def path(self):
        return 'airlines.graphml'

    def sanitize(self, g):
        d = {}
        for node, data in g.nodes(data=True):
            d[node] = data['tooltip'].split('(')[0]
        nx.set_node_attributes(g, d, 'name')
        return g


if __name__ == '__main__':
    g = AirlineDemo().get_graph()

    pos = {n: (d['x'], d['y']) for n, d in g.nodes.items()}
    nx.draw(g, pos, node_size=10)
    plt.show()
