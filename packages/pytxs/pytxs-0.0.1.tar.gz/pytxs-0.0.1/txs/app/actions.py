"""QAction used by txs application"""

from __future__ import annotations


from silx.gui import icons, qt


class SaveMainWindowAction(qt.QAction):
    """QAction to save a MainWindow central widget as a PNG file"""

    def __init__(self, parent: qt.QMainWindow | None = None):
        super().__init__()
        self.setParent(parent)
        self.setIcon(icons.getQIcon("document-save"))
        self.setText("Save as...")
        self.setToolTip("Save plot snapshot dialog")

        self.setShortcut(qt.QKeySequence.Save)
        self.setShortcutContext(qt.Qt.WidgetShortcut)
        self.triggered.connect(self._saveCentralWidgetToPng)

    def setParent(self, parent: qt.QMainWindow | None):
        self.setEnabled(parent is not None)
        return super().setParent(parent)

    def _saveCentralWidgetToPng(self):
        parent = self.parent()
        if parent is None:
            return

        filename = qt.QFileDialog.getSaveFileName(
            parent,
            caption="Save plot snapshot",
            dir="txs_snapshot.png",
            filter="Images (*.png)",
            options=qt.QFileDialog.DontUseNativeDialog,
        )
        if isinstance(filename, tuple):  # PyQt5
            filename = filename[0]

        if not filename:
            return
        if not filename.lower().endswith(".png"):
            filename = filename + ".png"

        centralWidget = parent.centralWidget()
        pixmap = centralWidget.grab()
        pixmap.save(filename)


class CopyMainWindowAction(qt.QAction):
    """QAction to copy a MainWindow central widget to clipboard"""

    def __init__(self, parent: qt.QMainWindow | None = None):
        super().__init__()
        self.setParent(parent)
        self.setIcon(icons.getQIcon("edit-copy"))
        self.setText("Copy plot")
        self.setToolTip("Copy a snapshot of the plot into the clipboard")

        self.setShortcut(qt.QKeySequence.Copy)
        self.setShortcutContext(qt.Qt.WidgetShortcut)
        self.triggered.connect(self._copyCentralWidgetToClipboard)

    def setParent(self, parent: qt.QMainWindow | None):
        self.setEnabled(parent is not None)
        return super().setParent(parent)

    def _copyCentralWidgetToClipboard(self):
        parent = self.parent()
        if parent is None:
            return

        centralWidget = parent.centralWidget()
        pixmap = centralWidget.grab()
        image = pixmap.toImage()
        qt.QApplication.clipboard().setImage(image)
