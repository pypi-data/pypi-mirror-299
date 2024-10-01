from __future__ import annotations

from collections.abc import Iterable
import itertools

import numpy as np

import silx
from silx.gui import qt
from silx.gui.plot import items
from silx.gui.plot.LegendSelector import LegendIcon
from silx.gui.plot.tools.PositionInfo import PositionInfo

from . import utils
from .PlotBase import PlotBase


class _LegendWidget(qt.QWidget):
    """Widget displaying the style, legend of a curve with extra info"""

    clicked = qt.Signal()
    """Signal emitted when this widget is clicked"""

    def __init__(self, curve: items.Curve, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.__curve = curve
        self.__curve.sigItemChanged.connect(self.__curveChanged)

        layout = qt.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        layout.addWidget(LegendIcon(curve=self.__curve))

        self.__label = qt.QLabel(self.__curve.getName())
        self.__label.setAlignment(qt.Qt.AlignLeft | qt.Qt.AlignVCenter)
        layout.addWidget(self.__label)

    def __curveChanged(self, event: items.ItemChangedType):
        if event == items.ItemChangedType.VISIBLE:
            self.__label.setEnabled(self.getCurve().isVisible())

    def getCurve(self) -> items.Curve:
        """Returns the curve item this widget represents"""
        return self.__curve

    def setInfo(self, info: str):
        """Set extra information displayed with the curve legend"""
        legend = self.getCurve().getName()
        if info:
            legend = f"{legend} ({info})"
        self.__label.setText(legend)

    def mouseReleaseEvent(self, event: qt.QMouseEvent):
        if event.button() != qt.Qt.LeftButton:
            return
        position = event.pos()
        if 0 <= position.x() <= self.width() and 0 <= position.y() <= self.height():
            self.clicked.emit()


class _CurveLegendsWidget(qt.QWidget):
    """Widget displaying a list of curve legends with extra information"""

    curveClicked = qt.Signal(items.Curve)
    """Signal emitted when a curve's legend is clicked"""

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

    def clear(self):
        """Clear all legends from the list"""
        for widget in self.children():
            if isinstance(widget, _LegendWidget):
                widget.setParent(None)

    def __legendWidgetClicked(self):
        legendWidget = self.sender()
        self.curveClicked.emit(legendWidget.getCurve())

    def setCurve(self, curve: items.Curve, info: str):
        """Add or update a curve to the list of legends with the given extra information

        If the curve legend was not displayed yet, it is appended.
        If it was already displayed, it's extra information is updated.
        """
        for widget in self.children():
            if isinstance(widget, _LegendWidget) and curve is widget.getCurve():
                break
        else:  # No legend widget for this curve: add it
            widget = _LegendWidget(curve)
            widget.clicked.connect(self.__legendWidgetClicked)
            self.layout().addWidget(widget)
        widget.setInfo(info)

    def removeCurve(self, curve: items.Curve):
        """Remove the legend corresponding to the given curve if present"""
        for widget in self.children():
            if isinstance(widget, _LegendWidget) and curve is widget.getCurve():
                widget.setParent(None)
                return


class _PlotCurves(PlotBase):
    """Widget to display curves sharing the same x with their legend"""

    CURVE_COLORS_AND_STYLES = tuple(
        (color, linestyle)
        for linestyle in ("-", "--", "-.", ":")
        for color in silx.config.DEFAULT_PLOT_CURVE_COLORS
    )
    """Sequence of default curve's (color, style)"""

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)

        self.__x = np.array([])
        self.__legends = ()
        self.__y = np.array([[]])
        self.__yerrors = np.array([[]])
        self.__info = ()

        plotWidget = self.getPlotWidget()
        plotWidget.setDataMargins(0.01, 0.01, 0.05, 0.05)
        plotWidget.setGraphGrid(True)

        sideWidget = qt.QWidget()
        sideLayout = qt.QVBoxLayout(sideWidget)
        self.centralWidget().layout().addWidget(sideWidget)

        sideLayout.addWidget(qt.QLabel("Legends:"))
        self.__legendsWidget = _CurveLegendsWidget()
        self.__legendsWidget.setMinimumWidth(150)
        self.__legendsWidget.curveClicked.connect(
            lambda curve: curve.setVisible(not curve.isVisible())
        )
        sideLayout.addWidget(self.__legendsWidget)
        sideLayout.addStretch(1)

        self.__positionInfo = PositionInfo(parent=None, plot=plotWidget)
        self.statusBar().addWidget(self.__positionInfo)

    def setAxesLabels(self, xlabel: str, ylabel: str):
        """Set abscissa and ordinate axes labels"""
        plotWidget = self.getPlotWidget()
        plotWidget.getXAxis().setLabel(xlabel)
        plotWidget.getYAxis().setLabel(ylabel)

        self.statusBar().removeWidget(self.__positionInfo)
        self.__positionInfo = PositionInfo(
            parent=None,
            plot=plotWidget,
            converters=[(xlabel, lambda x, y: x), (ylabel, lambda x, y: y)],
        )
        self.statusBar().addWidget(self.__positionInfo)

    def _updateAxesConstraints(
        self,
        x: np.ndarray,
        y: np.ndarray,
        yerror: np.ndarray,
    ):
        """Update axes constraint according to given data and current margins"""
        plotWidget = self.getPlotWidget()
        margins = plotWidget.getDataMargins()

        xfinite = x[np.isfinite(x)]
        lowerYErrors = y - yerror
        lowerYErrorsFinite = lowerYErrors[np.isfinite(lowerYErrors)]
        upperYErrors = y + yerror
        upperYErrorsFinite = upperYErrors[np.isfinite(upperYErrors)]
        if (
            xfinite.size == 0
            or lowerYErrorsFinite.size == 0
            or upperYErrorsFinite.size == 0
        ):
            plotWidget.getXAxis().setLimitsConstraints()
            plotWidget.getYAxis().setLimitsConstraints()
            return

        xmin = np.min(xfinite)
        xmax = np.max(xfinite)
        xextent = xmax - xmin
        plotWidget.getXAxis().setLimitsConstraints(
            xmin - margins[0] * xextent,
            xmax + margins[1] * xextent,
        )

        ymin = np.min(lowerYErrorsFinite)
        ymax = np.max(upperYErrorsFinite)
        yextent = ymax - ymin
        plotWidget.getYAxis().setLimitsConstraints(
            ymin - margins[2] * yextent,
            ymax + margins[3] * yextent,
        )

    def _updateCurve(
        self,
        legend: str,
        x: np.ndarray,
        y: np.ndarray,
        yerror: np.ndarray | None = None,
        info: str = "",
        color: str | qt.QColor | None = None,
        linestyle: str | None = "-",
    ) -> items.Curve:
        """Update (Create if legend do not exit) a curve"""
        plot = self.getPlotWidget()

        curve = plot.addCurve(
            x,
            y,
            legend=legend,
            color=color,
            linestyle=linestyle,
            yerror=yerror,
            selectable=False,
            resetzoom=False,
        )
        if isinstance(curve, str):  # silx v1
            curve = plot.getCurve(curve)
        self.__legendsWidget.setCurve(curve, info)
        return curve

    def _updateCurves(
        self,
        x: np.ndarray,
        legends: Iterable[str],
        y: np.ndarray,
        yerrors: np.ndarray,
        info: Iterable[str],
    ):
        """Override in subclass to change data used for curves display"""
        self._updateAxesConstraints(x, y, yerrors)
        for legend, ydata, yerror, text, (color, linestyle) in zip(
            legends, y, yerrors, info, itertools.cycle(self.CURVE_COLORS_AND_STYLES)
        ):
            self._updateCurve(legend, x, ydata, yerror, text, color, linestyle)

    def getData(
        self, copy: bool = True
    ) -> tuple[np.ndarray, tuple[str, ...], np.ndarray, np.ndarray, tuple[str, ...]]:
        """Return currently displayed curves data"""
        return (
            np.array(self.__x, copy=copy or utils.NP_OPTIONAL_COPY),
            self.__legends,
            np.array(self.__y, copy=copy or utils.NP_OPTIONAL_COPY),
            np.array(self.__yerrors, copy=copy or utils.NP_OPTIONAL_COPY),
            self.__info,
        )

    def setData(
        self,
        x: np.ndarray,
        legends: Iterable[str],
        y: np.ndarray,
        yerrors: np.ndarray,
        info: Iterable[str] | None,
        copy: bool = True,
    ):
        """Set curves data to plot.

        :param x: 1D array of x values
        :param legends: Curves legend, one per column of y and yerrors
            Used as curve identifier.
        :param y:
            Curves signal as a 2D array of shape: (nb legends, nb x)
        :param yerrors: 2D:
            Curves errors as a 2D array of shape: (nb legends, nb x)
        :param info: Extra information to display with the legend
        :param copy:
            Whether or not to make copy of ndarray arguments.
            If False, do not modify provided arrays.
        """
        resetZoom = len(self.__legends) == 0

        self.__x = np.array(x, copy=copy or utils.NP_OPTIONAL_COPY)
        self.__legends = tuple(legends)
        self.__y = np.array(y, copy=copy or utils.NP_OPTIONAL_COPY)
        self.__yerrors = np.array(yerrors, copy=copy or utils.NP_OPTIONAL_COPY)
        self.__info = ("",) * len(self.__legends) if info is None else tuple(info)
        self._updateCurves(
            self.__x, self.__legends, self.__y, self.__yerrors, self.__info
        )

        if resetZoom:
            self.getPlotWidget().resetZoom()

    def clear(self):
        """Remove all curves from the plot"""
        self.__x = np.array([])
        self.__legends = ()
        self.__y = np.array([[]])
        self.__yerrors = np.array([[]])
        self.__info = ()

        self.__legendsWidget.clear()

        self.setTitle("")
        plotWidget = self.getPlotWidget()
        plotWidget.getXAxis().setLimitsConstraints(None, None)
        plotWidget.getYAxis().setLimitsConstraints(None, None)
        plotWidget.clear()
        plotWidget.resetZoom()


class PlotIntensities(_PlotCurves):
    """Plot intensities+/-errors vs q"""

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.__averageCurve = None
        self.__delays = ()
        self.setWindowTitle("Intensities")
        self.setAxesLabels(xlabel=utils.Q_LABEL, ylabel=utils.I_LABEL)

    def setAverage(
        self,
        x: np.ndarray,
        y: np.ndarray,
        yerror: np.ndarray | None = None,
        info: str = "",
    ):
        """Set the average curve"""
        # Set the color so it does not consume one of the default list
        self.__averageCurve = self._updateCurve(
            "Average", x, y, yerror, info, "black", "--"
        )
        self.__averageCurve.setLineWidth(2)
        self._updateAverageCurveColor()

    def setDataFromDict(self, results: dict):
        """Set displayed curves from datared result"""
        # Transpose results arrays
        intensities = np.transpose(results["i"])
        errors = np.transpose(results["e"])

        if tuple(results["t"]) != self.__delays:
            self.clear()
            self.__delays = tuple(results["t"])

        # Retrieve last index of available each delay
        availableDelays = results["delays"][: len(intensities)]
        selectedIndices = [
            int(np.nonzero(availableDelays == delay)[0][-1])
            for delay in results["t"]
            if delay in availableDelays
        ]

        self.setTitle(utils.titleFromResults(results))
        self.setAverage(
            x=results["q"],
            y=np.mean(intensities, axis=0),
            yerror=None,
            info=f"{len(intensities)} frames",
        )
        self.setData(
            x=results["q"],
            legends=[results["delays"][index] for index in selectedIndices],
            y=intensities[selectedIndices],
            yerrors=errors[selectedIndices],
            info=[f"frame {index}" for index in selectedIndices],
            copy=False,
        )

    def clear(self):
        self.__averageCurve = None
        self.__delays = ()
        super().clear()

    def _updateAverageCurveColor(self):
        """Set the color of the average curve according to the current palette"""
        if self.__averageCurve is not None:
            palette = self.palette()
            color = palette.color(qt.QPalette.Text)
            self.__averageCurve.setColor(color)

    def changeEvent(self, event: qt.QEvent):
        super().changeEvent(event)
        if event.type() == qt.QEvent.PaletteChange:
            self._updateAverageCurveColor()


class PlotDifferences(PlotIntensities):
    """Plot time-resolved azimuthal intensity differences"""

    _DELTA_I = "ΔI"
    _Q_DELTA_I = "q*ΔI"

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.__delays = ()
        self.setWindowTitle("Time-Resolved Differences")

        self.setAxesLabels(xlabel=utils.Q_LABEL, ylabel=self._DELTA_I)

        toolbar = self.getToolsToolBar()
        toolbar.addWidget(qt.QLabel("Y Axis:"))
        self.__comboBox = qt.QComboBox()
        self.__comboBox.addItem(self._DELTA_I)
        self.__comboBox.addItem(self._Q_DELTA_I)
        self.__comboBox.setCurrentIndex(0)
        self.__comboBox.currentTextChanged.connect(self._currentTextChanged)
        toolbar.addWidget(self.__comboBox)

    def _updateCurves(
        self,
        x: np.ndarray,
        legends: Iterable[str],
        y: np.ndarray,
        yerrors: np.ndarray,
        info: Iterable[str],
    ):
        """Multiply deltaI by q for 'q*ΔI' mode"""
        if self.__comboBox.currentText() == self._DELTA_I:
            return super()._updateCurves(x, legends, y, yerrors, info)
        # Multiple intensities by q
        return super()._updateCurves(x, legends, x * y, yerrors, info)

    def _currentTextChanged(self, text: str):
        self.setAxesLabels(xlabel=utils.Q_LABEL, ylabel=text)
        self._updateCurves(*self.getData(copy=False))
        self.getPlotWidget().resetZoom()

    def setDataFromDict(self, results: dict):
        """Set displayed curves from datared result"""
        if "filt_res" in results:
            info = [f"{selected}/{total}" for selected, total in results["filt_res"]]
        else:
            info = None

        if tuple(results["t"]) != self.__delays:
            self.clear()
            self.__delays = tuple(results["t"])

        self.setTitle(utils.titleFromResults(results))
        self.setData(
            x=results["q"],
            legends=results["t"],
            info=info,
            y=np.transpose(results["diff_av"]),
            yerrors=np.transpose(results["diff_err"]),
            copy=False,
        )

    def clear(self):
        self.__delays = ()
        super().clear()
