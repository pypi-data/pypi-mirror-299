import os

import pytest

import numpy as np

from txs.datasets import ImageIteratorHDF5, load_images, BlissDataset

path = os.path.dirname(os.path.abspath(__file__))


def test_load_edf_images(edf_data_path):
    imgs, fnames = load_images(
        edf_data_path, 
        extension='edf', 
        exclude=["run01_0004.edf"], 
        return_fnames=True
    )
    assert np.sum(imgs) == 1082970310
    assert len(fnames) == 5


def test_load_bliss_images(bliss_scan_path):
    imgs, fnames = load_images(
        bliss_scan_path, 'h5', return_fnames=True
    )
    assert all(imgs.shapes[0] == [2, 1920, 1920])
    assert len(fnames) == 15


@pytest.mark.xfail(raises=TypeError)
def test_bliss_dataset_file_error(bliss_dataset):
    assert isinstance(bliss_dataset[1], ImageIteratorHDF5)


def test_bliss_dataset_metadata(bliss_dataset):
    assert np.allclose(
        bliss_dataset.metadata(12)['delay'], 
        [-5e-5, 1e-3, 10e-5] * 10
    )


def test_bliss_dataset_scan_paths(bliss_dataset, bliss_scan_path):
    assert (
        bliss_dataset._get_scan_paths()['12.1'] == 
        os.path.abspath(bliss_scan_path)
    )


@pytest.mark.xfail(raises=NotImplementedError)
def test_bliss_dataset_filter(bliss_dataset):
    bliss_dataset.filter(images=lambda x: 0)


def test_bliss_scan_slice(bliss_scan):
    assert bliss_scan[:10].sum() == 1478169543


def test_bliss_scan_counters(bliss_scan):
    bliss_scan.counters = "all"
    assert np.allclose(bliss_scan[0]["rayonix_roi1_max"], 359.0)
