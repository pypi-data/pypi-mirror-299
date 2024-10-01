from __future__ import annotations

import numpy as np

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import actions, items
from silx.gui.plot.ColorBar import ColorBarWidget
from silx.gui.plot.tools.PositionInfo import PositionInfo
from silx.utils.weakref import WeakMethodProxy

from . import utils
from .PlotBase import PlotBase


class PlotHeatmap(PlotBase):
    """Widget to display an array of integrated curves as an image"""

    _YLABEL = "Frame index"

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)

        self.__x = np.array([])
        self.__data = np.array([[]])

        plotWidget = self.getPlotWidget()
        plotWidget.setDefaultColormap(Colormap("viridis"))
        plotWidget.getXAxis().setLabel(utils.Q_LABEL)
        plotWidget.getYAxis().setLabel(self._YLABEL)
        plotWidget.getYAxis().setLimitsConstraints(0, None)

        colorBarWidget = ColorBarWidget()
        colorBarWidget.setPlot(plotWidget)
        colorBarWidget.setLegend(utils.I_LABEL)
        self.centralWidget().layout().addWidget(colorBarWidget)

        self.__positionInfo = PositionInfo(
            parent=None,
            plot=plotWidget,
            converters=[
                (utils.Q_LABEL, lambda x, y: x),
                (utils.I_LABEL, WeakMethodProxy(self._getImageValue)),
                (self._YLABEL, WeakMethodProxy(self._getFrameIndex)),
            ],
        )
        self.statusBar().addWidget(self.__positionInfo)

        # Toolbars
        toolsToolBar = self.getToolsToolBar()
        toolsToolBar.addAction(actions.control.ColormapAction(plotWidget, toolsToolBar))

    def _getFrameIndex(self, x: float, y: float) -> int | str:
        """Check that y corresponds to a frame index

        :param x: X position in plot coordinates
        :param y: Y position in plot coordinates
        :return: The frame index or '-'
        """
        if 0 <= y < len(self.__data):
            return int(y)
        return "-"

    def _getImageValue(self, x: float, y: float) -> float | str:
        """Get value of top most image at position (x, y)

        :param x: X position in plot coordinates
        :param y: Y position in plot coordinates
        :return: The value at that point or '-'
        """
        plotWidget = self.getPlotWidget()
        for picked in plotWidget.pickItems(
            *plotWidget.dataToPixel(x, y, check=False),
            lambda item: isinstance(item, items.ImageBase),
        ):
            image = picked.getItem()
            indices = picked.getIndices(copy=False)
            if indices is not None:
                row, col = indices[0][0], indices[1][0]
                value = image.getData(copy=False)[row, col]
                return value

        return "-"  # No image picked

    def getData(self, copy: bool = True) -> tuple[np.ndarray, np.ndarray]:
        """Return currently displayed data"""
        return (
            np.array(self.__x, copy=copy or utils.NP_OPTIONAL_COPY),
            np.array(self.__data, copy=copy or utils.NP_OPTIONAL_COPY),
        )

    def setData(
        self,
        x: np.ndarray,
        data: np.ndarray,
        copy: bool = True,
    ):
        """Set data to plot.

        :param x: 1D array of x values
        :param data:
            Curves signal as a 2D array of shape: (nb curves, nb x)
        :param copy:
            Whether or not to make copy of ndarray arguments.
            If False, do not modify provided arrays.
        """
        self.__x = np.array(x, copy=copy or utils.NP_OPTIONAL_COPY)
        self.__data = np.array(data, copy=copy or utils.NP_OPTIONAL_COPY)

        plotWidget = self.getPlotWidget()
        yDataRange = plotWidget.getDataRange().y
        isYZoomed = (
            yDataRange is not None and yDataRange != plotWidget.getYAxis().getLimits()
        )

        plotWidget.addImage(
            self.__data,
            origin=(self.__x[0], 0),
            scale=((self.__x[-1] - self.__x[0]) / len(x), 1),
            legend="data",
            resetzoom=False,
        )
        updated = plotWidget.getXAxis().setLimitsConstraints(self.__x[0], self.__x[-1])
        if not isYZoomed or updated:
            plotWidget.resetZoom()

    def showEvent(self, event: qt.QShowEvent) -> None:
        self.getPlotWidget().resetZoom()
        return super().showEvent(event)

    def clear(self):
        """Remove the image from the plot"""
        self.__x = np.array([])
        self.__data = np.array([[]])

        self.setTitle("")
        plotWidget = self.getPlotWidget()
        plotWidget.getXAxis().setLimitsConstraints(None, None)
        plotWidget.clear()
        plotWidget.resetZoom()

    def setDataFromDict(self, results: dict):
        """Set heatmap from datared result"""
        self.setTitle(utils.titleFromResults(results))
        self.setData(x=results["q"], data=np.transpose(results["i"]))
