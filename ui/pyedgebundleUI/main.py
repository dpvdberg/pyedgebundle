import sys
from threading import Thread
from xml.etree import ElementTree

import easygui
import matplotlib
import networkx as nx
from PySide2 import QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from matplotlib import pyplot as plt

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm
from data.interpolation.BSplineInterpolate import BSplineInterpolate
from parse.GraphUtils import GraphUtils
from ui.EBCanvas import EBCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from ui.pyedgebundleUI.utils.AntBundleParameterSettings import AntBundleParameterSettings, AntBundleParameters

matplotlib.use('Qt5Agg')


class Form(QMainWindow):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        self.path = None
        self.graph = None
        self.algorithm = None
        self.thread = None
        self.parameters = AntBundleParameterSettings().getValues()

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Menu bar
        self.ui.menuFileOpen.triggered.connect(self.openFile)
        self.ui.btnSettings.clicked.connect(self.settings)
        self.ui.btnRun.clicked.connect(lambda: self.run(open_file=True))

        # Matplotlib widget
        content = self.ui.widget

        self.canvas = EBCanvas()

        self.ntb = NavigationToolbar(self.canvas, self)

        content_box = QVBoxLayout()
        content_box.addWidget(self.canvas)
        content_box.addWidget(self.ntb)

        content.setLayout(content_box)

        self.info: QLabel = self.ui.lblInfo

        self.canvas.draw()
        self.ui.show()

    def settings(self):
        dlg = AntBundleParameterSettings(self.parameters)
        if dlg.exec_() == QDialog.Accepted:
            self.parameters = dlg.getValues()

    def create_bundler(self):
        return AntBundleAlgorithm(
            self.graph,
            self.create_interpolator(),
            self.parameters.runs,
            self.parameters.numberOfSegments,
            self.parameters.decreaseByConstant,
            self.parameters.decreaseFactor,
            self.parameters.randomness,
            self.parameters.threshold,
            self.parameters.updateDistance,
            self.parameters.pathExponent
        )

    def create_interpolator(self):
        return BSplineInterpolate(
            max_degree=self.parameters.splineInterpolationDegree
        )

    def bundle(self):
        parameters = AntBundleParameters(**self.parameters.__dict__)

        self.algorithm = self.create_bundler()
        self.bundled_graph = self.algorithm.bundle()

        self.canvas.update_bundled_graph(self.bundled_graph)

    def run(self, open_file=True):
        if self.path and self.graph:
            self.thread = Thread(target=self.bundle)
            self.thread.start()
        elif open_file:
            self.openFile()
            self.run(open_file=False)

    def openFile(self):
        self.path = easygui.fileopenbox()

        if not self.path:
            return

        try:
            g = nx.read_graphml(self.path)
        except (nx.NetworkXError, ElementTree.ParseError) as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(str(e))

            error_dialog.exec_()
            return

        g, success = GraphUtils.sanitize(g)
        if success:
            self.graph = g
            self.setGraphInfo()
            self.canvas.update_plain_graph(self.graph)
        else:
            self.path = None

    def setGraphInfo(self):
        if not self.graph:
            return

        max_x, max_y, _ = GraphUtils.getGraphFieldShape(self.graph)
        node_count = len(self.graph.nodes)

        self.info.setText(f"#nodes: {node_count}\tdimensions: ({max_x}, {max_y})")


if __name__ == '__main__':
    app = QApplication()
    form = Form('form.ui')
    sys.exit(app.exec_())
