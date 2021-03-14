from typing import Tuple

import networkx as nx
from PySide2.QtWidgets import QDialog

from ui.pyedgebundleUI.utils.graphMLPropertySelector import graphMLPropertySelector


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
    def sanitize(g: nx.Graph) -> (nx.Graph, bool):
        properties = GraphUtils.getCommonProperties(g)
        if {'x', 'y', 'name'}.issubset(properties):
            return g, True

        dlg = graphMLPropertySelector(properties)
        if dlg.exec_() == QDialog.Accepted:
            ps = dlg.value
            d = {}
            for node, data in g.nodes(data=True):
                d[node] = {
                    'x': data[ps.x],
                    'y': data[ps.y],
                    'hasName': ps.useName,
                    'name': data[ps.name] if ps.useName else ''
                }
            nx.set_node_attributes(g, d)
            return g, True
        else:
            return g, False

        # We need to ask the user to specify these properties or skip the name

    @staticmethod
    def getGraphFieldShape(g: nx.Graph) -> Tuple[int, int, int]:
        return max(data['x'] for _, data in g.nodes(data=True)) + 1, \
               max(data['y'] for _, data in g.nodes(data=True)) + 1, \
               max(n for n in g.nodes) + 1
