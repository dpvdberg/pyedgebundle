from typing import Optional

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from data.BundledGraph import BundledGraph
import networkx as nx

from parse.GraphUtils import GraphUtils


class EBCanvas(FigureCanvas):
    def __init__(self):
        self.bg: Optional[BundledGraph] = None
        self.g: Optional[nx.Graph] = None
        self.fig, self.ax = plt.subplots()
        super(EBCanvas, self).__init__(self.fig)

    def update_bundled_graph(self, bg: BundledGraph):
        self.bg = bg
        self.ax.cla()
        self.bg.plot(fig=self.fig, ax=self.ax, show=False)
        self.draw()

    def update_plain_graph(self, g: nx.Graph):
        self.g = g
        self.ax.cla()
        nx.draw_networkx(self.g, GraphUtils.createPositionDict(g), ax=self.ax)
        self.ax.set_aspect('equal')
        self.draw()
