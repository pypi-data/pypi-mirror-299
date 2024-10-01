import os

import pytest

import numpy as np

from txs.azav import integrate1d_dataset
from txs.utils import get_ai, load_mask
from txs.datared import datared


path = os.path.dirname(os.path.abspath(__file__))


# different set of keyword arguments to be tested
_TEST_KEYWORDS = dict(
    ai=get_ai(15e3, 0.350, (960, 960), detector='rayonix', binning=(2, 2)),
    mask=load_mask(path + "/sample_data/mask.edf"),
    error_model='poisson',
)


def test_edf_datared(edf_data_path):
    azav = integrate1d_dataset(edf_data_path, **_TEST_KEYWORDS)
    red = datared(azav, 'auto', norm=(2.1, 2.2), red_chi2_max=5)
    assert np.allclose(red['diff_av'].sum(), -4.620663285255432)