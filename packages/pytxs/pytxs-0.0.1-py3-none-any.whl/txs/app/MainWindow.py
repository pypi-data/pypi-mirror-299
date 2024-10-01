from __future__ import annotations

import logging
import os
import pprint
from collections.abc import Callable
from copy import deepcopy

import numpy as np
import pyFAI.units
from silx.gui import qt
from silx.gui.qt import inspect as qt_inspect
from tqdm import tqdm

from txs import get_ai
from txs.app.ProcessWorker import ProcessWorker
from txs.app.utils import WheelEventFilter
from txs.corr import get_mu, material_in_xraydb
from txs.azav import integrate1d_dataset
from txs.datared import datared
from txs.live import ana
from txs.utils import load_mask


_logger = logging.getLogger(__name__)


BINNINGS = 1, 2, 3, 4, 5, 6, 8, 10


DETECTORS = {
    "rayonix": {
        "display_name": "Rayonix MX170-HS",
        "intensity_offset": 10,
        "binning_enabled": True,
        "binning": "2x2",
        "shape": (3840, 3840),
    },
    "jungfrau1m": {
        "display_name": "Jungfrau 1M",
        "intensity_offset": 0,
        "binning_enabled": False,
        "binning": "1x1",
        "shape": (1064, 1032),
    },
}


def run_ana(
    put: Callable,
    ai_pars: dict,
    azav_pars: dict,
    datared_pars: dict,
    live: bool = False,
    verbose: bool = False,
):
    """Function to execute date reduction in a separate process and report progress"""
    # Monkey-patch tqdm to retrieve progress
    tqdm_display = tqdm.display

    def display(obj, *args, **kwargs):
        put({"type": "progress", "n": obj.n, "total": obj.total})
        tqdm_display(obj, *args, **kwargs)

    tqdm.display = display

    if not live:
        azav = integrate1d_dataset(ai=get_ai(**ai_pars), **azav_pars)
        result = datared(azav, **datared_pars)
        put(result)
        return

    # Run data reduction live
    class Callback:
        """ana callback with an emit method"""

        @staticmethod
        def emit(result):
            put(deepcopy(result))

    qlim = datared_pars.pop("qlim")
    ana(
        result_callback=Callback,
        sleep_loop=1,
        ai=get_ai(**ai_pars),
        verbose=verbose,
        qlim_azav=qlim,
        qlim_datared=qlim,
        **azav_pars,
        **datared_pars,
    )


class _ProgressBar(qt.QProgressBar):
    """Progress bar displaying progress as current / total"""

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.setMaximumWidth(self.sizeHint().width())
        self.setFormat("%v / %m")

    def setEnabled(self, enabled: bool) -> None:
        if not enabled:
            self.setRange(0, 1)
            self.reset()
        return super().setEnabled(enabled)

    def setUndetermined(self) -> None:
        """Set progress bar to undetermined progress state"""
        self.setRange(0, 0)

    def setProgress(self, value: int, total: int) -> None:
        """Set progress as value / total"""
        if value >= total:
            self.setUndetermined()
            return
        self.setMaximum(total)
        self.setValue(value)


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__error = ""

        qt.loadUi(
            os.path.join(os.path.dirname(__file__), "mainwindow.ui"),
            baseinstance=self,
        )
        self._progressBar = _ProgressBar()
        self._progressBar.setEnabled(False)
        self.statusBar().addPermanentWidget(self._progressBar)

        self._worker = ProcessWorker()
        self._worker.taskAboutToStart.connect(self._workerStarting)
        self._worker.taskStopped.connect(self._workerStopped)
        self._worker.valueChanged.connect(self._resultChanged)

        # Populate binning combo box
        for binning in BINNINGS:
            self.binningComboBox.addItem(f"{binning}x{binning}", (binning, binning))

        for name, info in DETECTORS.items():
            self.detectorComboBox.addItem(info["display_name"], name)
            self.detectorComboBox.setCurrentIndex(0)

        # Tweak style
        self.errorAction.setIcon(
            self.style().standardIcon(qt.QStyle.SP_MessageBoxWarning)
        )

        self.openAction.triggered.connect(self._openData)
        self.errorAction.triggered.connect(self._errorActionClicked)
        self.inputBrowseButton.clicked.connect(self._openData)
        self.processPushButton.clicked.connect(self._processPushButtonClicked)
        self.processExtraPushButton.started.connect(self._start)
        self.maskPushButton.clicked.connect(self._maskPushButtonClicked)
        self.intensityOffsetResetToolButton.clicked.connect(self._resetIntensityOffset)
        self.detectorComboBox.currentIndexChanged.connect(self._detectorChanged)
        self.binningComboBox.currentIndexChanged.connect(self._resetCenter)
        self.binningComboBox.currentIndexChanged.connect(self._updateImageShape)
        self.photonEnergyDoubleSpinBox.valueChanged.connect(self._updateWavelength)
        self.photonEnergyDoubleSpinBox.valueChanged.connect(self._updateSampleMu)
        self.sampleMaterialLineEdit.editingFinished.connect(self._updateSampleMu)

        self.imageFilterToolButton.toggled.connect(self._sectionToolButtonToggled)
        self.azimuthalAverageToolButton.toggled.connect(self._sectionToolButtonToggled)
        self.absorptionCorrectionToolButton.toggled.connect(
            self._sectionToolButtonToggled
        )
        self.dataSelectToolButton.toggled.connect(self._sectionToolButtonToggled)
        self.timeAverageToolButton.toggled.connect(self._sectionToolButtonToggled)

        self._detectorChanged()
        self._updateWavelength()

        # Disable wheel interaction for widgets inside the scroll area
        wheelEventFilter = WheelEventFilter(self)
        wheelEventFilter.filter(
            self.parametersScrollArea.findChildren(
                (qt.QComboBox, qt.QDoubleSpinBox, qt.QSpinBox)
            )
        )

        self.resize(800, 600)

    def _openData(self):
        path = qt.QFileDialog.getExistingDirectory(
            self,
            caption="txs - Select Data Folder",
            directory="",
        )
        if path:
            self.setInputFolder(path)

    def _start(self, mode: str = "process"):
        self.processPushButton.setChecked(True)
        kwargs = self.parameters(force=mode == "reprocess")
        _logger.info(f"Start processing:\n{pprint.pformat(kwargs)}")
        self.plotIntensities.clear()
        self.plotHeatmap.clear()
        self.plotDifferences.clear()
        self._worker.start(run_ana, kwargs=kwargs)

    def _processPushButtonClicked(self, checked: bool):
        if checked:
            self._start()
            return

        _logger.info("Stop processing")
        self._worker.stop()

    def _maskPushButtonClicked(self):
        filename = qt.QFileDialog.getOpenFileName(
            self,
            "Open Mask File...",
            "",
            "NumPy (*.npy);;EDF (*.edf);;All (*.*)",
        )[0]
        if filename:
            self.maskLineEdit.setText(filename)

    def _resetIntensityOffset(self):
        defaultOffset = DETECTORS[self.detector()]["intensity_offset"]
        self.intensityOffsetSpinBox.setValue(defaultOffset)

    def _detectorChanged(self):
        detectorInfo = DETECTORS[self.detector()]

        self._resetIntensityOffset()
        self.darkGroupBox.setChecked(detectorInfo["intensity_offset"] != 0)
        self.binningComboBox.setCurrentText(detectorInfo["binning"])
        self.binningComboBox.setEnabled(detectorInfo["binning_enabled"])
        self._resetCenter()
        self._updateImageShape()

    def _resetCenter(self):
        rows, columns = self.imageShape()
        self.centerXDoubleSpinBox.setValue(columns / 2)
        self.centerYDoubleSpinBox.setValue(rows / 2)

    def _updateSampleMu(self):
        material = self.sampleMaterialLineEdit.text()
        if not material:
            self.sampleMuLineEdit.setText("")
            return

        if not material_in_xraydb(material):
            self.sampleMuLineEdit.setText("Not available")
            return

        sample_mu = get_mu(material, self.energyInEV())
        self.sampleMuLineEdit.setText(f"{sample_mu/1e2:.2}")

    def _sectionToolButtonToggled(self, checked):
        toolButton = self.sender()
        # ArrowDown if checked else ArrowRight
        # TODO check with the different version of PyQt/PySide
        toolButton.setArrowType(qt.Qt.ArrowType(2) if checked else qt.Qt.ArrowType(4))

    def _updateImageShape(self):
        rows, columns = self.imageShape()
        self.imageShapeLineEdit.setText(f"({rows}, {columns})")

    def _updateWavelength(self):
        wavlength = pyFAI.units.CONST_hc / (self.energyInEV() * 1e-3)
        self.wavelengthLineEdit.setText(f"{wavlength:.4}")

    def _workerStarting(self):
        self.statusBar().showMessage(f"Data processing starting", 3000)
        self._progressBar.setEnabled(True)

    def _workerStopped(self):
        if not qt_inspect.isValid(self):
            return

        if qt_inspect.isValid(self.processPushButton):
            self.processPushButton.setChecked(False)

        statusBar = self.statusBar()
        if qt_inspect.isValid(statusBar):
            statusBar.showMessage(f"Data processing stopped", 3000)

        if qt_inspect.isValid(self._progressBar):
            self._progressBar.setEnabled(False)

    def _resultChanged(self, result: dict):
        if not qt_inspect.isValid(self):
            return

        if result.get("type", "") == "progress":
            self._progressBar.setProgress(result["n"], result["total"])
            return

        self._progressBar.setUndetermined()

        self.plotIntensities.setDataFromDict(result)
        self.plotHeatmap.setDataFromDict(result)
        self.plotDifferences.setDataFromDict(result)

    def _errorActionClicked(self):
        button = qt.QMessageBox.warning(
            self,
            "Error",
            self.getError(),
            qt.QMessageBox.Reset | qt.QMessageBox.Close,
            qt.QMessageBox.Close,
        )
        if button == qt.QMessageBox.Reset:
            self.setError("")

    def getError(self) -> str:
        """Returns error information string"""
        return self.__error

    def setError(self, error: str):
        """Set error information string"""
        if error == self.__error:
            return

        self.__error = error
        if qt_inspect.isValid(self):
            self.errorAction.setVisible(error != "")

    def binning(self) -> tuple[int, int]:
        """Returns the currently selected image binning"""
        return self.binningComboBox.currentData()

    def detector(self) -> str:
        """Returns currently selected detector"""
        return self.detectorComboBox.currentData()

    def energyInEV(self) -> float:
        """Returns photon energy in eV"""
        return self.photonEnergyDoubleSpinBox.value() * 1e3

    def imageShape(self) -> tuple[int, int]:
        """Returns image shape for current detector and binning"""
        rows, columns = DETECTORS[self.detector()]["shape"]
        binning = self.binning()
        if binning is None:
            return rows, columns
        return rows // binning[0], columns // binning[1]

    def parameters(self, force: bool = False) -> dict:
        """Returns current processing parameters"""

        # Azimuthal integration parameters
        ai_pars = {
            "energy": self.energyInEV(),
            "distance": 1e-3 * self.distanceDoubleSpinBox.value(),
            "center": (
                self.centerXDoubleSpinBox.value(),
                self.centerYDoubleSpinBox.value(),
            ),
            "detector": self.detector(),
            "binning": self.binning(),
            "pixel": None,
        }

        # azav parameters
        azav_pars = {
            "folder": self.inputLineEdit.text(),
            "save_fname": self.ouputLineEdit.text(),
            "force": force,
        }

        if self.zingerGroupBox.isChecked():
            azav_pars["dezinger_method"] = "mask_zingers"
            azav_pars["dezinger"] = (
                self.intensityThresholdSpinBox.value(),
                self.clusterRadiusSpinBox.value(),
            )
        else:
            azav_pars["dezinger"] = None

        maskFilename = self.maskLineEdit.text()
        if maskFilename:
            azav_pars["mask"] = load_mask(maskFilename)  # TODO handle errors
        else:
            azav_pars["mask"] = None

        if self.darkAutomaticRadioButton.isChecked():
            azav_pars["dark"] = "auto"
        elif self.darkOffsetRadioButton.isChecked():
            intensityOffset = self.intensityOffsetSpinBox.value()
            azav_pars["dark"] = intensityOffset * np.ones(
                self.imageShape(), dtype=np.float32
            )
        else:
            azav_pars["dark"] = None

        azav_pars["npt"] = self.radialBinsSpinBox.value()
        azav_pars["method"] = self.integrationMethodComboBox.currentText()

        if self.sampleGroupBox.isChecked():
            azav_pars["sample_material"] = self.sampleMaterialLineEdit.text()
            azav_pars["sample_thickness"] = (
                1e-6 * self.sampleThicknessDoubleSpinBox.value()
            )
        else:
            azav_pars["sample_material"] = None
            azav_pars["sample_thickness"] = None

        # Data reduction
        datared_pars = {}

        if self.sliceGroupBox.isChecked():
            datared_pars["shots"] = (
                self.firstSliceSpinBox.value(),
                self.lastSliceSpinBox.value(),
            )
        else:
            datared_pars["shots"] = None

        if self.qRangeGroupBox.isChecked():
            qlim = (
                self.qRangeMinDoubleSpinBox.value(),
                self.qRangeMaxDoubleSpinBox.value(),
            )
        else:
            qlim = None
        datared_pars["qlim"] = qlim

        datared_pars["ref_delay"] = self.referenceLineEdit.text()

        if self.qRangeRadioButton.isChecked():
            datared_pars["norm"] = (
                self.minQRangeNormalizationDoubleSpinBox.value(),
                self.maxQRangeNormalizationDoubleSpinBox.value(),
            )
        elif self.parameterRadioButton.isChecked():
            datared_pars["norm"] = self.parameterLineEdit.text()
        else:  # Disabled
            datared_pars["norm"] = None

        if self.outliersFilterAutoRadioButton.isChecked():
            datared_pars["red_chi2_max"] = "auto"
            datared_pars["pts_perc_max"] = None
        elif self.outliersFilterReducedChi2RadioButton.isChecked():
            datared_pars["red_chi2_max"] = (
                self.outliersFilterReducedChi2DoubleSpinBox.value()
            )
            datared_pars["pts_perc_max"] = None
        elif self.outliersFilterFractionRadioButton.isChecked():
            datared_pars["red_chi2_max"] = None
            datared_pars["pts_perc_max"] = (
                self.outliersFilterFractionDoubleSpinBox.value()
            )
        else:  # Disabled
            datared_pars["red_chi2_max"] = None
            datared_pars["pts_perc_max"] = None

        return {
            "ai_pars": ai_pars,
            "azav_pars": azav_pars,
            "datared_pars": datared_pars,
            "live": self.processLiveCheckBox.isChecked(),
            "verbose": _logger.getEffectiveLevel() <= logging.INFO,
        }

    def setInputFolder(self, folder: str):
        self.inputLineEdit.setText(folder)

    def setOutputFilename(self, filename: str):
        self.ouputLineEdit.setText(filename)

    def setMaskFilename(self, filename: str):
        self.maskLineEdit.setText(filename)

    # Settings

    _SETTINGS_VERSION_STR = "1"

    def closeEvent(self, event):
        settings = qt.QSettings()
        settings.setValue("version", self._SETTINGS_VERSION_STR)
        settings.setValue("mainwindow/geometry", self.geometry())
        settings.setValue("mainwindow/fullscreen", self.isFullScreen())
        settings.setValue("mainwindow/splitter/sizes", self.splitter.sizes())
        settings.setValue("parameters/folder", self.inputLineEdit.text())
        settings.setValue("parameters/save_fname", self.ouputLineEdit.text())
        settings.setValue("parameters/mask", self.maskLineEdit.text())
        settings.setValue("parameters/live", self.processLiveCheckBox.isChecked())

    def _setFullScreen(self, enabled: bool):
        """Toggle the window state to full screen"""
        if enabled:
            self.setWindowState(qt.Qt.WindowFullScreen)
        elif self.isFullScreen():
            self.setWindowState(qt.Qt.WindowNoState)

    def loadSettings(self):
        """Load user settings"""
        settings = qt.QSettings()
        if settings.value("version") != self._SETTINGS_VERSION_STR:
            settings.clear()
            return

        for key, func in {
            "mainwindow/geometry": self.setGeometry,
            "mainwindow/fullscreen": lambda ison: self._setFullScreen(ison == "true"),
            "mainwindow/splitter/sizes": lambda sizes: self.splitter.setSizes(
                [int(size) for size in sizes]
            ),
            "parameters/folder": self.setInputFolder,
            "parameters/save_fname": self.setOutputFilename,
            "parameters/mask": self.setMaskFilename,
            "parameters/live": lambda ison: self.processLiveCheckBox.setChecked(
                ison == "true"
            ),
        }.items():
            value = settings.value(key)
            if value is not None:
                func(value)
