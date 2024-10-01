"""A QObject that runs a function in a separate process and reports its life-cycle"""

from __future__ import annotations

from collections.abc import Callable
import logging
import multiprocessing
import os
import queue
import signal
import threading
import traceback

from silx.gui import qt
from silx.gui.utils.concurrent import submitToQtMainThread


_logger = logging.getLogger(__name__)


class ProcessWorker(qt.QObject):
    """Run a target function providing updates in a separate processus"""

    taskAboutToStart = qt.Signal()
    """Signal emitted when the separate processus is about to start"""

    taskStopped = qt.Signal()
    """Signal emitted when the separate processus has stopped"""

    valueChanged = qt.Signal(object)
    """Signal emitted each time the target function reports a new result"""

    def __init__(self, parent: qt.QObject | None = None):
        super().__init__(parent)
        self.__thread = None
        self.__process = None
        qt.QApplication.instance().aboutToQuit.connect(self.stop)

    def __del__(self):
        self.stop()

    def isRunning(self) -> bool:
        """Returns whether a process is running or not"""
        return self.__process is not None

    def __queueReader(
        self,
        process: multiprocessing.Process,
        q: multiprocessing.Queue,
    ):
        """Wait and read from queue to emit resultChanged

        Returns when the queue is closed.
        """
        while process.is_alive():
            try:
                result = q.get(block=True, timeout=0.5)
            except queue.Empty:
                continue
            except ValueError:
                break  # Queue is closed, stop here
            # Signal is emitted in the thread that instantiated ProcessWorker
            self.valueChanged.emit(result)

        # Make sure to stop the process and reset state
        submitToQtMainThread(self.stop)

    @staticmethod
    def _runInProcess(target, queue, **kwargs):
        """Method run in the separate process"""
        # Make sure to use default Ctrl-C handling
        signal.signal(signal.SIGINT, signal.default_int_handler)

        # Notify main process
        queue.put("READY")

        try:
            target(queue.put, **kwargs)
        except KeyboardInterrupt:
            pass  # Received sigint
        except BaseException as e:
            print("Exception raised in process", type(e), e)
            traceback.print_exc()
        finally:
            queue.close()
            queue.join_thread()

    def start(self, target: Callable, kwargs: dict | None = None):
        """Start executing target in a separate process

        :param target:
           A callable that will receive as first argument a callable with the same signature as
           `queue.Queue.put <https://docs.python.org/3/library/queue.html#queue.Queue.put>`_
           and otherwise **kwargs.
        """
        if self.isRunning():
            raise RuntimeError("Process already running")

        context = multiprocessing.get_context("spawn")
        queue_ = context.Queue(maxsize=1)
        self.__process = context.Process(
            target=self._runInProcess,
            args=(target, queue_),
            kwargs={} if kwargs is None else kwargs,
        )
        self.__thread = threading.Thread(
            target=self.__queueReader, args=(self.__process, queue_)
        )

        self.taskAboutToStart.emit()

        self.__process.start()
        queue_.get(block=True)  # Wait for ready message
        self.__thread.start()

    def stop(self):
        if not self.isRunning():
            return

        # Stop process
        if self.__process.is_alive():
            # Send Ctrl+C
            os.kill(self.__process.pid, signal.SIGINT)
            self.__process.join(2)
            if self.__process.exitcode is None:
                _logger.error("Cannot close process nicely")
                # TODO close the queue and the thread first?
                self.__process.kill()  # Send SIGKILL
        self.__process = None

        # Wait for thread to stop
        if self.__thread is not None:
            self.__thread.join(2)
            if self.__thread.is_alive():
                _logger.error("Cannot stop queue reader thread")
        self.__thread = None

        self.taskStopped.emit()
