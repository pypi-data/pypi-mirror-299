import os

import pytest

from txs.datasets import BlissDataset, ImageIteratorHDF5


path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def edf_data_path():
    return path + "/sample_data/edf/"


@pytest.fixture
def bliss_data_path():
    return path + "/sample_data/bliss/dye1/dye1_0002"


@pytest.fixture
def bliss_scan_path():
    return path + "/sample_data/bliss/dye1/dye1_0002/scan0012"


@pytest.fixture
def bliss_dataset():
    dset_file_path = "/sample_data/bliss/dye1/dye1_0002/dye1_0002.h5"
    return BlissDataset(path + dset_file_path)


@pytest.fixture
def bliss_scan():
    return ImageIteratorHDF5(
        path + "/sample_data/bliss/dye1/dye1_0002/scan0012/"
    )