import os
import pathlib
import sys
from threading import Thread
from typing import Optional
from xml.etree import ElementTree

import easygui
import matplotlib
import networkx as nx
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, Signal, QObject, Slot, QCoreApplication, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from matplotlib.figure import Figure

from algorithms.AntBundleAlgorithm import AntBundleAlgorithm
from algorithms.ProgressCallback import ProgressCallback
from data.BundledGraph import BundledGraph
from data.PheromoneField import PheromoneField
from data.interpolation.BSplineInterpolate import BSplineInterpolate
from parse.GraphUtils import GraphUtils
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ui.pyedgebundleUI.utils.AntBundleOutputWindow import AntBundleOutputWindow
from ui.pyedgebundleUI.utils.AntBundleParameterSettings import AntBundleParameterSettings, AntBundleParameters

matplotlib.use('Qt5Agg')


# Signals must inherit QObject
class Communicate(QObject):
    update_progress = Signal(float, float, str)
    bundle_result = Signal(BundledGraph, PheromoneField, AntBundleParameters)


class Form(QMainWindow, ProgressCallback):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        self.communicate = Communicate()
        self.communicate.update_progress.connect(self.emit_progress)
        self.communicate.bundle_result.connect(self.bundle_result)

        self.path = None
        self.graph = None
        self.algorithm = None
        self.thread: Optional[Thread] = None
        self.stopped = False
        self.parameters = AntBundleParameterSettings().getValues()

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Menu bar
        self.ui.menuFileOpen.triggered.connect(self.openFile)
        self.ui.btnSettings.clicked.connect(self.settings)
        self.ui.btnRun.clicked.connect(lambda: self.run(open_file=True))
        self.ui.btnStop.clicked.connect(self.stop)

        # Matplotlib widget
        content = self.ui.widget

        self.canvas = FigureCanvas(Figure((6, 7)))
        self.figure = self.canvas.figure
        self.ax = self.canvas.figure.subplots()
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.text(0.5, 0.5, 'No graph loaded', ha='center', va='center')

        self.ntb = NavigationToolbar(self.canvas, self)
        self.ntb.hide()

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

    @Slot(float, float, str)
    def emit_progress(self, overall, subtask_progress, subtask_name):
        self.ui.progressBarOverall.setValue(int(overall * 100))
        self.ui.progressBarSub.setValue(int(subtask_progress * 100))
        self.ui.lblSubtask.setText(subtask_name)

    def progress(self, overall, subtask_progress, subtask_name):
        # ask ui thread to handle progress update
        self.communicate.update_progress.emit(overall, subtask_progress, subtask_name)

    @Slot(BundledGraph, PheromoneField, AntBundleParameters)
    def bundle_result(self, bg: BundledGraph, pf: PheromoneField, parameters: AntBundleParameters):
        dlg = AntBundleOutputWindow(bg, pf, parameters, parent=self)
        dlg.show()

        self.ui.btnRun.setEnabled(True)
        self.ui.btnSettings.setEnabled(True)

    def bundle(self):
        parameters = AntBundleParameters(**self.parameters.__dict__)

        self.algorithm = self.create_bundler()
        self.algorithm.progress_callback = self
        bundled_graph = self.algorithm.bundle()

        if not self.stopped:
            self.communicate.bundle_result.emit(bundled_graph, self.algorithm.field, parameters)

        self.communicate.update_progress.emit(0, 0, "Waiting...")

    def run(self, open_file=True):
        if self.path and self.graph:
            self.stopped = False
            self.ui.btnRun.setEnabled(False)
            self.ui.btnSettings.setEnabled(False)

            self.thread = Thread(target=self.bundle)
            self.thread.start()
        elif open_file:
            self.openFile()
            self.run(open_file=False)

    def stop(self):
        if self.thread.is_alive() and self.algorithm:
            if easygui.ynbox('Do you want to terminate?', 'Stop request', ['Yes', 'No']):
                self.stopped = True
                self.algorithm.stop()

                self.ui.btnRun.setEnabled(True)
                self.ui.btnSettings.setEnabled(True)

    def draw(self):
        self.ntb.show()
        self.ax.cla()
        nx.draw_networkx(self.graph, GraphUtils.createPositionDict(self.graph),
                         ax=self.ax,
                         with_labels=False,
                         node_size=100)
        self.ax.set_aspect('equal')
        self.canvas.draw()

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
            self.draw()
        else:
            self.path = None

    def setGraphInfo(self):
        if not self.graph:
            return

        max_x, max_y, _ = GraphUtils.getGraphFieldShape(self.graph)
        node_count = len(self.graph.nodes)

        self.info.setText(f"#nodes: {node_count}\tdimensions: ({max_x}, {max_y})")


def start():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication()
    form = Form(os.path.join(pathlib.Path(__file__).parent.absolute(), "form.ui"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
