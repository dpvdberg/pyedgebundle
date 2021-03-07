from enum import Enum
import networkx as nx


class Demo(Enum):
    AIRLINE = 1

class

class pyedgebundleDemo:
    def path(self):
        return 'airlines.graphml'

    def sanitize(self, type):
        pass

    def get_graph(self):
        g = nx.read_graphml('data/{}')

        # Sanitize airlines graph
        d = {}
        for node, data in g.nodes(data=True):
            d[node] = data['tooltip'].split('(')[0]
        nx.set_node_attributes(g, d, 'name')


if __name__ == '__main__':
    pyedgebundleDemo().airlines()
