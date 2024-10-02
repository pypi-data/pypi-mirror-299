"""
Test methods for a xarray/cerbere BackendEntryPoint to read a dataset.

All these methods must be imported in the test module for the new
BackendEntryPoint. This test module must implement the following fixtures:

* test_file : return the input file to be used in this test
* download_url : return the url to test data repository
* backend : return the BackendEntryPoint class name
* feature : return the related feature class corresponding to the dataset
"""
import datetime
import os
from pathlib import Path

import pytest

import numpy
import xarray as xr

import cerbere
from cerbere.feature.cbasefeature import BaseFeature


TEST_SUBSET = 'test_subset.nc'


@pytest.fixture(scope='module')
def download_url():
    return 'ftp://ftp.ifremer.fr/ifremer/cersat/projects/cerbere/test_data/'


@pytest.fixture(scope='module')
def input_file(test_file, backend, download_url):
    # search test file
    if 'CERBERE_TESTDATA_REPOSITORY' not in os.environ:
        raise EnvironmentError(
            'CERBERE_TESTDATA_REPOSITORY environment variable is not set')
    rootpath = Path(os.environ['CERBERE_TESTDATA_REPOSITORY'])
    dirname = Path(backend.split('.')[-1])
    testfilepath = rootpath / dirname / test_file

    if not testfilepath.exists():
        raise IOError(
            f'Test file {test_file} was not found. Please download it from '
              f'{download_url} and place in {Path(rootpath /dirname)} folder')

    return testfilepath


@pytest.fixture(scope='module')
def dataset(input_file, backend):
    """Open file and create dataset object"""
    return xr.open_dataset(input_file, engine=backend)


@pytest.fixture(scope='module')
def output_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('output')


def test_open_file_as_dataset(dataset):
    """Test dataset instantiation with an input file"""
    assert isinstance(dataset, xr.Dataset)


def test_get_list_of_vars(dataset):
    """Test reading the list of fields"""
    for v in dataset.data_vars:
        assert isinstance(v, str)
        assert (v != "")


def test_read_vars(dataset):
    """Test reading and displaying variable properties"""
    vars = dataset.data_vars
    for v in vars:
        print(f'...reading {v}')
        assert isinstance(dataset.data_vars[v], xr.DataArray)
        print(dataset.data_vars[v])


def test_read_global_dimensions(dataset):
    """Test reading and displaying global dimensions"""
    print('...reading global dimensions')
    dims = dataset.dims

    assert dims is not None
    assert len(dims) > 0

    for dim in dims:
        dimsize = dataset.sizes[dim]
        print('.....', dim, dimsize)

        assert isinstance(dim, str)
        assert isinstance(dimsize, int)


def test_read_global_attributes(dataset):
    """Test reading the global attributes"""
    for attr in dataset.attrs:
        print(attr, dataset.attrs[attr])
        assert isinstance(dataset.attrs[attr],
                          (str, int, datetime.datetime, numpy.int32,
                           numpy.uint32, numpy.int16, numpy.float32,
                           numpy.float64, list))
