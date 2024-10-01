import os

import pytest

import numpy as np

from txs.utils import get_ai


path = os.path.dirname(os.path.abspath(__file__))


def test_get_ai():
    ai = get_ai(15e3, 0.350, (960, 960), detector='rayonix', binning=(2, 2))
    assert ai.get_pixel1() == 8.85417e-05