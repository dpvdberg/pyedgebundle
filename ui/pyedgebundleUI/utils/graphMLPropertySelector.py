from dataclasses import dataclass

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType
from PySide2.examples.webchannel.standalone.ui_dialog import Ui_Dialog

TestQDialog = loadUiType("utils/graphMLPropertySelector.ui")[0]


@dataclass
class SelectedProperties:
    x: str = ''
    y: str = ''
    name: str = ''
    useName: bool = True


class graphMLPropertySelector(QtWidgets.QDialog, TestQDialog):
    def __init__(self, properties, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.properties = properties
        self.setupUi(self)
        self.value: SelectedProperties = SelectedProperties()

        self.boxes = [self.cbX, self.cbY, self.cbName]

        for box in self.boxes:
            box.addItems(self.properties)

        self.btnbox.accepted.connect(self.tryAccept)
        self.btnbox.rejected.connect(QtWidgets.QDialog.reject)

    def tryAccept(self):
        self.setValues()
        if self.value:
            self.accept()

    def setValues(self):
        useName = not self.chkName.isChecked()

        if useName:
            valid = len({x.currentText() for x in self.boxes}) == 3
        else:
            valid = self.cbX.currentText() != self.cbY.currentText()

        if not valid:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Select unique properties for each requested attribute.")

            error_dialog.exec_()
            self.value = None
        else:
            self.value = SelectedProperties(
                self.cbX.currentText(),
                self.cbY.currentText(),
                self.cbName.currentText(),
                useName
            )
