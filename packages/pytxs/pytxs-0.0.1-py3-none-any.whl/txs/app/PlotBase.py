from __future__ import annotations

import silx

if silx.version_info.major < 2:  # Use matplotlib colors
    import matplotlib.colors

    silx.config.DEFAULT_PLOT_CURVE_COLORS = list(
        matplotlib.colors.TABLEAU_COLORS.values()
    )

if silx.version_info.major == 2:  # Use experimental feature
    silx.config._MPL_TIGHT_LAYOUT = True

from silx.gui import qt
from silx.gui.plot import actions, PlotWidget

from .actions import CopyMainWindowAction, SaveMainWindowAction


class PlotBase(qt.QMainWindow):
    """Widget plotting image and curves

    This is the base class of all plot in txs GUI
    """

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        if parent is not None:  # behave as a widget
            self.setWindowFlags(qt.Qt.Widget)

        centralWidget = qt.QWidget()
        # Use same background/foreground as the plot area
        centralWidget.setAutoFillBackground(True)
        centralWidget.setBackgroundRole(qt.QPalette.Base)
        centralWidget.setForegroundRole(qt.QPalette.Text)
        layout = qt.QHBoxLayout(centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralWidget)

        self.__plotWidget = PlotWidget()
        centralWidget.layout().addWidget(self.__plotWidget, stretch=1)
        self._updatePlotWidgetColors()

        # Toolbars
        self.__toolsToolBar = self.addToolBar("Tools")
        self.__toolsToolBar.setMovable(False)
        self.__toolsToolBar.addAction(
            actions.mode.ZoomModeAction(self.__plotWidget, self.__toolsToolBar)
        )
        self.__toolsToolBar.addAction(
            actions.mode.PanModeAction(self.__plotWidget, self.__toolsToolBar)
        )
        self.__toolsToolBar.addSeparator()
        self.__toolsToolBar.addAction(
            actions.control.ResetZoomAction(self.__plotWidget, self.__toolsToolBar)
        )

        exportToolBar = self.addToolBar("Export")
        exportToolBar.setMovable(False)
        spacer = qt.QWidget()
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        exportToolBar.addWidget(spacer)
        exportToolBar.addAction(CopyMainWindowAction(self))
        exportToolBar.addAction(SaveMainWindowAction(self))

    def getPlotWidget(self) -> PlotWidget:
        return self.__plotWidget

    def getToolsToolBar(self) -> qt.QToolBar:
        return self.__toolsToolBar

    def setTitle(self, title: str):
        """Set the plot title"""
        self.getPlotWidget().setGraphTitle(title)

    # Handle foreground/background colors

    def _updatePlotWidgetColors(self):
        palette = self.palette()
        plot = self.getPlotWidget()
        plot.setBackgroundColor(palette.color(qt.QPalette.Base))
        plot.setForegroundColor(palette.color(qt.QPalette.Text))

    def changeEvent(self, event: qt.QEvent):
        if event.type() == qt.QEvent.PaletteChange:
            self._updatePlotWidgetColors()
