import os
import pathlib
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtWidgets import QDialog
from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure

from data.BundledGraph import BundledGraph
from data.PheromoneField import PheromoneField
from ui.pyedgebundleUI.utils.AntBundleParameterSettings import AntBundleParameters, AntBundleParameterSettings
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

AntBundleOutputUI = \
    loadUiType(os.path.join(pathlib.Path(__file__).parent.absolute(), "AntBundleOutputWindow.ui"))[0]


class AntBundleOutputWindow(QtWidgets.QDialog, AntBundleOutputUI):
    def __init__(self, graph: BundledGraph, field: PheromoneField, parameters: AntBundleParameters, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.graph: BundledGraph = graph
        self.field: PheromoneField = field
        self.parameters: AntBundleParameters = parameters

        self.btnSettings.clicked.connect(self.show_settings)

        self.chkEdges.clicked.connect(self.update_drawing)
        self.chkPheromone.clicked.connect(self.update_drawing)

        # Matplotlib widget
        content = self.widget

        self.canvas = FigureCanvas(Figure())
        self.figure = self.canvas.figure
        self.ax = self.canvas.figure.subplots()

        self.ntb = NavigationToolbar(self.canvas, self)

        content_box = QVBoxLayout()
        content_box.addWidget(self.canvas)
        content_box.addWidget(self.ntb)

        content.setLayout(content_box)

        self.update_drawing()

    def update_drawing(self):
        self.ax.cla()
        for ax in self.figure.axes:
            if ax is not self.ax:
                ax.remove()

        if self.chkPheromone.isChecked():
            self.field.plot(fig=self.figure, ax=self.ax, show=False)

        # Draw nodes and (optionally) edges
        self.graph.plot(fig=self.figure, ax=self.ax, show=False, edges=self.chkEdges.isChecked())
        self.canvas.draw()

    def show_settings(self):
        dlg = AntBundleParameterSettings(self.parameters, read_only=True)
        dlg.exec_()
