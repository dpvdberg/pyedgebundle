from typing import Tuple

import networkx as nx
from PySide2.QtWidgets import QDialog

from ui.pyedgebundleUI.utils.GraphMLPropertySelector import GraphMLPropertySelector


class GraphUtils:
    @staticmethod
    def getCommonProperties(g: nx.Graph) -> list[str]:
        properties = None
        for n, data in g.nodes.items():
            if properties is None:
                properties = data.keys()

            properties = [key for key in properties if key in data]

        return properties

    @staticmethod
    def scale(g: nx.Graph, scale: float) -> nx.Graph:
        d = {}
        for node, data in g.nodes(data=True):
            d[node] = {
                'x': data['x'] * scale,
                'y': data['y'] * scale
            }
            nx.set_node_attributes(g, d)

        return g

    @staticmethod
    def integer_positions(g: nx.Graph) -> nx.Graph:
        d = {}
        for node, data in g.nodes(data=True):
            d[node] = {
                'x': int(data['x']),
                'y': int(data['y'])
            }
        nx.set_node_attributes(g, d)
        return g

    @staticmethod
    def sanitize(g: nx.Graph) -> (nx.Graph, bool):
        mapping = {n: i for i, n in enumerate(g.nodes)}
        g = nx.relabel_nodes(g, mapping)

        properties = GraphUtils.getCommonProperties(g)
        if {'x', 'y'}.issubset(properties):
            return GraphUtils.integer_positions(g), True

        dlg = GraphMLPropertySelector(properties)
        if dlg.exec_() == QDialog.Accepted:
            ps = dlg.value
            d = {}

            for node, data in g.nodes(data=True):
                d[node] = {
                    'x': int(data[ps.x]),
                    'y': int(data[ps.y]),
                    'hasName': ps.useName,
                    'name': data[ps.name] if ps.useName else ''
                }
            nx.set_node_attributes(g, d)

            neg_x = any(d['x'] < 0 for _, d in g.nodes(data=True))
            neg_y = any(d['y'] < 0 for _, d in g.nodes(data=True))
            if neg_x or neg_y:
                min_x = abs(min(d['x'] for _, d in g.nodes(data=True)))
                min_y = abs(min(d['y'] for _, d in g.nodes(data=True)))

                for node, data in g.nodes(data=True):
                    d[node] = {
                        'x': int(min_x + data['x']),
                        'y': int(min_y + data['y'])
                    }
                nx.set_node_attributes(g, d)

            return g, True
        else:
            return g, False

        # We need to ask the user to specify these properties or skip the name

    @staticmethod
    def createPositionDict(g: nx.Graph) -> dict:
        return {
            n: (d['x'], d['y']) for n, d in g.nodes(data=True)
        }

    @staticmethod
    def getGraphFieldShape(g: nx.Graph) -> Tuple[int, int, int]:
        return max(data['x'] for _, data in g.nodes(data=True)) + 1, \
               max(data['y'] for _, data in g.nodes(data=True)) + 1, \
               max(n for n in g.nodes) + 1
