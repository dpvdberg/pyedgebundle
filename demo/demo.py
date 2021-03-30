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
        mapping = {n: int(n) for n in g}
        g = nx.relabel_nodes(g, mapping)
        # tooltip -> name and integer x and y
        d = {}

        min_x = abs(min(d['x'] for _, d in g.nodes(data=True)))
        min_y = abs(min(d['y'] for _, d in g.nodes(data=True)))

        for node, data in g.nodes(data=True):
            d[node] = {'name': data['tooltip'].split('(')[0],
                       'x': int(min_x + data['x']),
                       'y': int(min_y + data['y'])}
        nx.set_node_attributes(g, d)
        return g


if __name__ == '__main__':
    g = AirlineDemo().get_graph()

    pos = {n: (d['x'], d['y']) for n, d in g.nodes.items()}
    nx.draw(g, pos, node_size=10)
    plt.show()
