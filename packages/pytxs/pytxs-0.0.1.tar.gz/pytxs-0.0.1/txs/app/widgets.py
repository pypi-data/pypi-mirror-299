from __future__ import annotations

from silx.gui import icons, qt


class ProcessPushButton(qt.QPushButton):
    """A QPushButton with an animated icon when checked"""

    def __init__(self, parent: qt.QWidget | None):
        super().__init__(parent)
        self._setStartIcon()

        self.__waitingIcons = icons.getWaitIcon()
        self.__waitingIcons.iconChanged.connect(self.setIcon)
        self.toggled.connect(self.__toggled)
        self.__toggled(self.isChecked())

    def _setStartIcon(self):
        self.setIcon(self.style().standardIcon(qt.QStyle.SP_MediaPlay))

    def __toggled(self, checked: bool):
        if checked:
            self.setIcon(self.__waitingIcons.currentIcon())
            self.__waitingIcons.register(self)
            self.setText("Stop")
            self.setToolTip("Stop data processing")
            return

        self.__waitingIcons.unregister(self)
        self._setStartIcon()
        self.setText("Process Data")
        self.setToolTip("Start data processing")


class ProcessExtraPushButton(qt.QPushButton):
    """QpushButton with a menu providing different processing modes"""

    started = qt.Signal(str)
    """Emitted when a menu action has been triggered by the user"""

    def __init__(self, parent: qt.QWidget | None):
        super().__init__(parent)
        menu = qt.QMenu(self)
        processAction = menu.addAction(
            self.style().standardIcon(qt.QStyle.SP_MediaPlay),
            "Process Data",
        )
        processAction.triggered.connect(self.__processActionTriggered)
        reprocessAction = menu.addAction(
            self.style().standardIcon(qt.QStyle.SP_BrowserReload),
            "Reprocess Data",
        )
        reprocessAction.triggered.connect(self.__reprocessActionTriggered)
        self.setMenu(menu)

    def __processActionTriggered(self):
        self.started.emit("process")

    def __reprocessActionTriggered(self):
        self.started.emit("reprocess")
