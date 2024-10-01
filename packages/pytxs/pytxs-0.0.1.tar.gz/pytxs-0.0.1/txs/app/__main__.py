from __future__ import annotations

import argparse
import logging
import traceback
import signal
import sys

from silx.gui import qt

from .MainWindow import MainWindow


logging.basicConfig()


_logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "inputFolder",
        metavar="FOLDER",
        help="Folder containing the images to process",
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="outputFilename",
        help="HDF5 filename where to store processed data",
        metavar="FILE",
    )
    parser.add_argument(
        "-m",
        "--mask",
        dest="maskFilename",
        help="Filename of the mask image",
        metavar="FILE",
    )
    parser.add_argument(
        "-f",
        "--fresh",
        dest="clearSettings",
        action="store_true",
        default=False,
        help="Do not load user preferences",
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )

    return parser.parse_args()


def main():
    """Create an execute the GUI"""
    options = parse_arguments()

    if options.verbose != 0:
        logging.getLogger().setLevel(
            logging.INFO if options.verbose == 1 else logging.DEBUG
        )

    app = qt.QApplication([])

    # Configure QSettings
    app.setOrganizationName("ESRF")
    app.setOrganizationDomain("esrf.fr")
    app.setApplicationName("txs")
    qt.QSettings.setDefaultFormat(qt.QSettings.IniFormat)

    if options.clearSettings:
        qt.QSettings().clear()

    window = MainWindow()
    window.setAttribute(qt.Qt.WA_DeleteOnClose, True)
    window.show()
    window.loadSettings()

    # Apply command line options
    if options.inputFolder:
        window.setInputFolder(options.inputFolder)
    if options.outputFilename:
        window.setOutputFilename(options.outputFilename)
    if options.maskFilename:
        window.setMaskFilename(options.maskFilename)

    # Set exception handler
    def exceptHook(type_, value, trace):
        _logger.error(f"An error occured in txs GUI: {type_.__name__} {value}")
        formattedTrace = "".join(traceback.format_tb(trace))
        _logger.error(formattedTrace)
        window.setError(f"{type_.__name__}:\n{value}\n\n{formattedTrace}")

    sys.excepthook = exceptHook

    def resetExceptHook():
        sys.excepthook = sys.__excepthook__

    app.aboutToQuit.connect(resetExceptHook)

    # Ignore Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    sys.exit(app.exec())


def main_txs2():
    print("txs2 is deprecated, use 'txs' instead to start the GUI")
    main()


if __name__ == "__main__":
    main()
