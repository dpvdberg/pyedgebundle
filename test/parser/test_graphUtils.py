from unittest import TestCase
import networkx as nx
from parser.GraphUtils import GraphUtils


class TestgraphUtils(TestCase):
    def test_get_common_properties(self):
        g = nx.read_graphml("../../examplegraphs/airlines.graphml")
        self.assertEqual(set(GraphUtils.getCommonProperties(g)), {'x', 'y', 'tooltip'})
