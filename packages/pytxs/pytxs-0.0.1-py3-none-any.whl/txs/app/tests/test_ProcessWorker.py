from __future__ import annotations

from collections.abc import Callable, Iterable
import time
from txs.app.ProcessWorker import ProcessWorker


def run(
    put_func: Callable,
    messages: Iterable = (),
    timeout: int = 0,
):
    """Function run by tests in a subprocess"""
    for message in messages:
        put_func(message)
        time.sleep(timeout / 1000)


def testComplete(qtbot):
    worker = ProcessWorker()

    with qtbot.waitSignals(
        (
            worker.taskAboutToStart,
            worker.valueChanged,
            worker.valueChanged,
            worker.taskStopped,
        ),
        check_params_cbs=(
            None,
            lambda value: value == 1,
            lambda value: value == 2,
            None,
        ),
        timeout=10000,
        order="strict",
    ):
        worker.start(run, kwargs={"messages": [1, 2]})

    assert not worker.isRunning()


def testStop(qtbot):
    worker = ProcessWorker()

    with qtbot.waitSignals(
        (worker.taskAboutToStart, worker.valueChanged),
        check_params_cbs=(None, lambda value: value == 1),
        timeout=10000,
        order="strict",
    ):
        worker.start(run, kwargs={"messages": [1, 2, 3], "timeout": 3000})

    with qtbot.waitSignal(worker.taskStopped, timeout=10000):
        worker.stop()

    assert not worker.isRunning()
