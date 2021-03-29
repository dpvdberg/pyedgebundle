import sys
from xml.etree import ElementTree

import easygui
import networkx as nx
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import QFile, Qt

import matplotlib

from parse.GraphUtils import GraphUtils
from ui.EBCanvas import EBCanvas

matplotlib.use('Qt5Agg')


class Form(QMainWindow):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Menu bar
        self.ui.menuFileOpen.triggered.connect(self.openFile)

        # Matplotlib widget
        mplWidget = self.ui.findChild(QWidget, 'mplWidget')
        layout = QVBoxLayout(mplWidget)

        self.canvas = EBCanvas()
        self.ui.setCentralWidget(self.canvas)

        self.ui.show()

    def openFile(self):
        path = easygui.fileopenbox()

        try:
            g = nx.read_graphml(path)
        except (nx.NetworkXError, ElementTree.ParseError) as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(str(e))

            error_dialog.exec_()
            return

        g, success = GraphUtils.sanitize(g)
        print(success)

if __name__ == '__main__':
    app = QApplication()
    form = Form('form.ui')
    sys.exit(app.exec_())
