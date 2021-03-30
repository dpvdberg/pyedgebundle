import os
import pathlib
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

import easygui
import clipboard
from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

AntBundleParametersUI = \
    loadUiType(os.path.join(pathlib.Path(__file__).parent.absolute(), "AntBundleParameterSettings.ui"))[0]


@dataclass_json
@dataclass
class AntBundleParameters:
    runs: int
    decreaseFactor: float
    decreaseByConstant: bool
    randomness: float
    threshold: float
    updateDistance: int
    pathExponent: int

    splineInterpolationDegree: int
    numberOfSegments: int


class AntBundleParameterSettings(QtWidgets.QDialog, AntBundleParametersUI):
    def __init__(self, parameters: Optional[AntBundleParameters] = None, parent=None, read_only=False):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.value: Optional[AntBundleParameters] = None

        self.btnbox.accepted.connect(self.tryAccept)
        self.btnbox.rejected.connect(self.reject)

        self.btnImport.clicked.connect(self.import_action)
        self.btnExport.clicked.connect(self.export_action)

        if parameters:
            self.setValues(parameters)

        if read_only:
            self.spnRuns.setReadOnly(True)
            self.spnDecreaseFactor.setReadOnly(True)
            origDecreaseByConstant = self.chkDecreaseByConstant.isChecked()
            self.chkDecreaseByConstant.clicked.connect(
                lambda: self.chkDecreaseByConstant.setChecked(origDecreaseByConstant))
            self.spnRandomness.setReadOnly(True)
            self.spnThreshold.setReadOnly(True)
            self.spnUpdateDistance.setReadOnly(True)
            self.spnPathExponent.setReadOnly(True)
            self.spnInterpolationDegree.setReadOnly(True)
            self.spnSegments.setReadOnly(True)

            self.btnImport.setEnabled(False)

    def tryAccept(self):
        self.value = self.getValues()
        self.accept()

    def setValues(self, parameters: AntBundleParameters):
        self.spnRuns.setValue(parameters.runs)
        self.spnDecreaseFactor.setValue(parameters.decreaseFactor)
        self.chkDecreaseByConstant.setChecked(parameters.decreaseByConstant)
        self.spnRandomness.setValue(parameters.randomness)
        self.spnThreshold.setValue(parameters.threshold)
        self.spnUpdateDistance.setValue(parameters.updateDistance)
        self.spnPathExponent.setValue(parameters.pathExponent)
        self.spnInterpolationDegree.setValue(parameters.splineInterpolationDegree)
        self.spnSegments.setValue(parameters.numberOfSegments)

    def getValues(self):
        return AntBundleParameters(
            self.spnRuns.value(),
            self.spnDecreaseFactor.value(),
            self.chkDecreaseByConstant.isChecked(),
            self.spnRandomness.value(),
            self.spnThreshold.value(),
            self.spnUpdateDistance.value(),
            self.spnPathExponent.value(),
            self.spnInterpolationDegree.value(),
            self.spnSegments.value()
        )

    def import_action(self):
        t = easygui.buttonbox('Where do you want to import from?', 'Import', ['File', 'Clipboard'])
        try:
            if t == 'File':
                path = easygui.fileopenbox(title="Settings location", default="ant_bundle_settings.json",
                                           filetypes=["*.json"])

                if not path:
                    return

                parameters_raw = open(path, 'r').read()
                parameters = AntBundleParameters.from_json(parameters_raw)
                self.setValues(parameters)

            elif t == 'Clipboard':
                parameters_raw = clipboard.paste()
                parameters = AntBundleParameters.from_json(parameters_raw)
                self.setValues(parameters)
        except:
            easygui.msgbox("Data does not represent valid parameter settings.", "Import error")

    def export_action(self):
        t = easygui.buttonbox('Where do you want to export to?', 'Export', ['File', 'Clipboard'])

        try:
            if t == 'File':
                path = easygui.filesavebox(title="Settings location", default="ant_bundle_settings.json",
                                           filetypes=["*.json"])

                if not path:
                    return

                open(path, 'w').write(self.getValues().to_json())

            elif t == 'Clipboard':
                clipboard.copy(self.getValues().to_json())
        except:
            easygui.msgbox("Could not export parameter settings.", "Export error")
