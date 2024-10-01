from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from silx.gui import qt


# Numpy v1/v2 array's copy argument compatibility
NP_OPTIONAL_COPY = False if np.version.version.startswith("1.") else None


Q_LABEL = "q (Å⁻¹)"
I_LABEL = "Scattered intensity (a.u.)"


def titleFromResults(results: dict) -> str:
    """Returns a title "dataset/scan" from datared result dict"""
    return "/".join(
        part
        for part in Path(results["azav"]["folder"]).absolute().parts[-2:]
        if part != "/"
    )


class WheelEventFilter(qt.QObject):
    """QObject that filters-out wheel events of registered widgets when they don't have focus"""

    def eventFilter(self, obj: qt.QObject, event: qt.QEvent) -> bool:
        """Event filter that filters-out wheel event for widget without focus"""
        if event.type() == qt.QEvent.Wheel:
            return not obj.hasFocus()
        return False

    def filter(self, widgets: Iterable[qt.QWidget]):
        """Install this event filter on the given widgets and disable focus on wheel events"""
        for widget in widgets:
            if widget.focusPolicy() == qt.Qt.FocusPolicy.WheelFocus:
                widget.setFocusPolicy(qt.Qt.FocusPolicy.StrongFocus)
            widget.installEventFilter(self)
