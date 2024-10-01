import os

import pytest

import numpy as np

from txs.azav import integrate1d, integrate1d_multi, integrate1d_dataset
from txs.utils import load_mask, get_ai
from txs.datasets import load_images


path = os.path.dirname(os.path.abspath(__file__))


# different set of keyword arguments to be tested
_TEST_KEYWORDS = [
    dict(
        ai=get_ai(15e3, 0.350, (960, 960), detector='rayonix', binning=(2, 2)),
        mask=load_mask(path + "/sample_data/mask.edf"),
        error_model='poisson',
    ),
    dict(
        ai=get_ai(15e3, 0.350, (960, 960), detector='rayonix', binning=(2, 2)),
        sample_material='H2O',
        sample_thickness=1.32e-3,
        dezinger=(40e3, 5),
    ),
]


# expected result for the first entry of the last integrated image
# for integrate1d, should be the value of 'res[1][0]'
# for integrate1d, should be the value of 'res[1][-1][0]'
_EXPECTED = [
    552.19604,
    264.0064,
    264.0064,
]


def test_get_ai():
    ai = get_ai(15e3, 0.350, (960, 960), detector='rayonix', binning=(2, 2))
    assert ai.get_pixel1() == 8.85417e-05


@pytest.mark.parametrize("kwargs,expected", zip(_TEST_KEYWORDS, _EXPECTED))
def test_edf_integrate1d(edf_data_path, kwargs, expected):
    imgs = load_images(edf_data_path, extension='edf')
    res = integrate1d(imgs[0], **kwargs)
    assert round(res[1][0]) == round(expected)


def test_edf_integrate1d_multi(edf_data_path):
    imgs = load_images(edf_data_path, extension='edf')
    res = integrate1d_multi(imgs, **_TEST_KEYWORDS[0])
    assert round(res[1][-1][0]) == round(546.69293)


def test_integrate_edf_dataset_with_force(edf_data_path):
    res = integrate1d_dataset(
        edf_data_path, 
        extension='edf',
        **_TEST_KEYWORDS[0],
        force=True
    )
    assert np.allclose(res['i'].sum(), 10003858.0)


def test_integrate_edf_dataset_no_force(edf_data_path):
    res = integrate1d_dataset(
        edf_data_path, 
        extension='edf',
        **_TEST_KEYWORDS[0],
    )
    assert np.allclose(res['i'].sum(), 10003858.0)


def test_h5_integrate1d_multi(bliss_scan_path):
    imgs = load_images(bliss_scan_path)
    res = integrate1d_multi(imgs[:2], **_TEST_KEYWORDS[0])
    assert np.allclose(res[1][-1].sum(), 152517.47)


def test_integrate_h5_dataset_with_force(bliss_scan_path):
    res = integrate1d_dataset(
        bliss_scan_path, 
        extension='h5', 
        **_TEST_KEYWORDS[0],
        force=True
    )
    assert np.allclose(res['i'].sum(), 6116991.0)


def test_integrate_h5_dataset_no_force(bliss_scan_path):
    res = integrate1d_dataset(
        bliss_scan_path, 
        extension='h5', 
        **_TEST_KEYWORDS[0],
    )
    assert np.allclose(res['i'].sum(), 6116991.0)
