import os
import pathlib
from dataclasses import dataclass
from typing import Optional

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

AntBundleParametersUI = \
    loadUiType(os.path.join(pathlib.Path(__file__).parent.absolute(), "AntBundleParameterSettings.ui"))[0]


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
    def __init__(self, parameters: Optional[AntBundleParameters] = None, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.value: Optional[AntBundleParameters] = None

        self.btnbox.accepted.connect(self.tryAccept)
        self.btnbox.rejected.connect(QtWidgets.QDialog.reject)

        if parameters:
            self.spnRuns.setValue(parameters.runs)
            self.spnDecreaseFactor.setValue(parameters.decreaseFactor)
            self.chkDecreaseByConstant.setChecked(parameters.decreaseByConstant)
            self.spnRandomness.setValue(parameters.randomness)
            self.spnThreshold.setValue(parameters.threshold)
            self.spnUpdateDistance.setValue(parameters.updateDistance)
            self.spnPathExponent.setValue(parameters.pathExponent)
            self.spnInterpolationDegree.setValue(parameters.splineInterpolationDegree)
            self.spnSegments.setValue(parameters.numberOfSegments)

    def tryAccept(self):
        self.value = self.getValues()
        self.accept()

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
