"""
Test methods for a xarray/cerbere reader classes for specific datasets.

All these methods must be imported in the test module for the new
reader. This test module must implement the following fixtures:

* test_file : return the input file to be used in this test
* download_url : return the url to test data repository
* reader : return the reader class name
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
from cerbere.feature.cbasecollection import BaseCollection


TEST_SUBSET = 'test_subset.nc'


@pytest.fixture(scope='module')
def download_url():
    return 'ftp://ftp.ifremer.fr/ifremer/cersat/projects/cerbere/test_data/'


@pytest.fixture(scope='module')
def input_file(test_file, reader, download_url):
    # search test file
    if 'CERBERE_TESTDATA_REPOSITORY' not in os.environ:
        rootpath = Path('tests/data/')
    else:
        rootpath = Path(os.environ['CERBERE_TESTDATA_REPOSITORY'])
    dirname = Path(reader.split('.')[-1])
    testfilepath = rootpath / dirname / test_file

    if not testfilepath.exists():
        raise IOError(
            f'Test file {test_file} was not found. Please download it from '
              f'{download_url} and place in {Path(rootpath /dirname)} folder')

    return testfilepath


@pytest.fixture(scope='module')
def dataset(input_file, reader):
    """Open file and create dataset object"""
    return cerbere.open_dataset(input_file, reader=reader)


@pytest.fixture(scope='module')
def feature_class():
    return


@pytest.fixture(scope='module')
def feature(input_file, reader):
    return cerbere.open_feature(input_file, reader=reader)


@pytest.fixture(scope='module')
def output_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('output')


def test_open_file_as_dataset(dataset, input_file):
    """Test dataset instantiation with an input file"""
    assert isinstance(dataset, xr.Dataset)
    assert dataset.cb.url == input_file


def test_open_file_as_feature(feature, feature_class):
    """Test dataset instantiation with an input file"""
    assert isinstance(feature, feature_class)

    if issubclass(feature_class, BaseCollection):
        assert feature.instance_class is not None


def test_open_dataset_and_feature(input_file, feature_class, reader):
    feature = cerbere.open_feature(
        input_file, feature_class.__name__, reader)
    assert isinstance(feature, BaseFeature)


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


def test_read_lat(dataset):
    """Test reading latitude and checking validity"""
    print('fillvalue', dataset['lat'].cb.fill_value)
    data = dataset['lat'].to_masked_array()

    print('...test there are no fillvalues')
    assert data.size == data.count()

    print('...test values are in valid range')
    assert -90 <= data.min() <= 90
    assert -90 <= data.max() <= 90


def test_read_lon(dataset):
    """Test reading longitude and checking validity"""
    data = dataset['lon'].to_masked_array()

    print('...test there are no fillvalues')
    assert data.size == data.count()

    print('...test values are in valid range')
    assert -180 <= data.min() <= 180
    assert -180 <= data.max() <= 180


def test_read_time(dataset):
    """Test reading time and checking validity"""
    def dt64todatetime(dt64):
        unix_epoch = numpy.datetime64(0, 's')
        one_second = numpy.timedelta64(1, 's')
        seconds_since_epoch = (dt64 - unix_epoch) / one_second
        return datetime.datetime.utcfromtimestamp(seconds_since_epoch)

    data = dataset['time'].to_masked_array()

    print('...test there are no fillvalues')
    assert data.size == data.count()
    assert isinstance(data.min(), numpy.datetime64)

    print('...test values are in valid range')
    time_min = dt64todatetime(data.min())
    print(data.min(), data.min().astype(datetime.datetime))
    print(f'...min time: {time_min} {type(time_min)}, {data.min()} '
          f'{type(data.min())}')
    assert time_min > datetime.datetime(1970, 1, 1)

    time_max = dt64todatetime(data.max())
    print('...max time: ', time_max)
    assert time_max < datetime.datetime(2050, 1, 1)


def test_read_global_attributes(dataset):
    """Test reading the global attributes"""
    for attr in dataset.attrs:
        print(attr, dataset.attrs[attr])
        assert isinstance(dataset.attrs[attr],
                          (str, int, datetime.datetime, numpy.int32, numpy.int8, numpy.int64,
                           numpy.uint32, numpy.int16, numpy.float32,
                           numpy.float64, list))


def test_read_time_coverage(dataset):
    """Test reading the coverage start end end time"""
    start = dataset.cb.time_coverage_start
    print('...start time : ', start)
    assert isinstance(start, datetime.datetime)

    end = dataset.cb.time_coverage_end
    print('...end time : ', end)
    assert isinstance(end, datetime.datetime)


def __extract_subset(feature, feature_class):
    """Extract a subset from a datamodel structure loaded with a file"""
    datasetobj = feature.dataset

    if feature.__class__.__name__ in ['Swath', 'Image']:
        cells = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['X']]
        rows = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['Y']]
        width = min(min(rows // 2, cells // 2), 5)
        r0, r1 = rows // 2 - width, rows // 2 + width
        c0, c1 = cells // 2 - width, cells // 2 + width
        slices = {feature.ds.cb.cf_axis_dims['Y']: slice(r0, r1, 1),
                  feature.ds.cb.cf_axis_dims['X']: slice(c0, c1, 1)}
        print('Subset: ', slices)
        subset = feature.isel(slices)

    elif feature.__class__.__name__ in ['Grid', 'GridTimeSeries']:
        if feature.is_cylindrical():
            ni = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['X']]
            nj = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['Y']]
            width = min(min(nj // 2, ni // 2), 5)
            j0, j1 = nj // 2 - width, nj // 2 + width
            i0, i1 = ni // 2 - width, ni // 2 + width
            subset = feature.isel(
                {'lat': slice(j0, j1, 1), 'lon': slice(i0, i1, 1)})
        else:
            ni = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['X']]
            nj = feature.ds.cb.cf_dims[feature.ds.cb.cf_axis_dims['Y']]
            width = min(min(nj // 2, ni // 2), 5)
            j0, j1 = nj // 2 - width, nj // 2 + width
            i0, i1 = ni // 2 - width, ni // 2 + width
            subset = feature.isel(
                {'y': slice(j0, j1, 1), 'x': slice(i0, i1, 1)})

    elif feature.__class__.__name__ in ['Trajectory']:
        times = feature.ds.dims[feature.ds.cb.cf_axis_dims['T']]
        width = min(times // 2, 5)
        r0, r1 = times // 2 - width, times // 2 + width
        print('Subset ')
        print('time : ', r0, r1)
        subset = feature.isel({'time': slice(r0, r1, 1)})

    elif feature.__class__.__name__ in ['TrajectoryProfile']:
        i_axis = feature.ds.cb.cf_instance_dims[0]
        z_axis = feature.ds.cb.cf_axis_dims['Z']
        times = feature.ds.dims[i_axis]
        z = feature.ds.dims[z_axis]
        width = min(times // 2, 5)
        r0, r1 = times // 2 - width, times // 2 + width
        subset = feature.isel(
            {i_axis: slice(r0, r1, 1), z_axis: slice(0, z // 2)})

    elif feature.__class__.__name__ in ['TimeSeriesProfile']:
        i_axis = feature.ds.cb.cf_instance_dims[0]
        z_axis = feature.ds.cb.cf_axis_dims['Z']
        times = feature.ds.dims[i_axis]
        z = feature.ds.dims[z_axis]
        width = min(times // 2, 5)
        r0, r1 = times // 2 - width, times // 2 + width
        subset = feature.isel(
            {i_axis: slice(r0, r1, 1), z_axis: slice(0, z // 2)})

    elif feature.__class__.__name__ in ['IMDCollection', 'OMDCollection']:
        instance_dim  = feature.ds.cb.cf_instance_dims[0]
        instances = feature.ds.dims[instance_dim]
        width = min(instances // 2, 5)
        r0, r1 = instances // 2 - width, instances // 2 + width
        if r0 == r1:
            r1 += 1
        subset = feature.isel(
            {instance_dim: slice(r0, r1, 1)})

    else:
        raise NotImplementedError

    assert isinstance(subset, feature_class)

    return subset


def test_extract_and_save_a_subset(feature, feature_class, output_dir):
    """Test extracting a subset from a file with feature and saving it"""
    # extract
    subset = __extract_subset(feature, feature_class)

    # test saving the subset in netCDF format
    fname = output_dir / TEST_SUBSET
    print(f'Output dir: {fname}')

    subset.dataset.cb.save(fname)

    # try reading the subset to check it si correctly formatted
    featureobj = feature_class(xr.open_dataset(fname))
    assert isinstance(featureobj, feature_class)
