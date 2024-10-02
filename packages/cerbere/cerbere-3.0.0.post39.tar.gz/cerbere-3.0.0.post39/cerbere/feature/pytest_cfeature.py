"""
Base class for unitary testing of cerbere feature classes with pytest.
"""
from datetime import datetime
import logging
from pathlib import Path

import pytest

import numpy as np
import xarray as xr

import cerbere
from cerbere.feature.cbasecollection import BaseCollection


logger = logging.getLogger()
logger.setLevel('DEBUG')


@pytest.fixture(scope='module')
def output_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('output')


@pytest.fixture(scope='module')
def instance_class():
    return


@pytest.fixture
def input_file(output_dir, feature_instance):

    # creates a test xarray object
    feat = feature_instance

    # save it to disk
    fname = Path(output_dir) /'test_feature_dataset.nc'
    if fname.exists():
        fname.unlink()
    feat.dataset.cb.save(fname)

    return Path(output_dir) /'test_feature_dataset.nc'


@pytest.fixture
def output_file(output_dir):
    return Path(output_dir) / 'test_saved_feature.nc'


@pytest.fixture
def test_var():
    return 'my_var'


@pytest.fixture
def test_create_feature_from_dict(feature_class, feature_instance):
    basefeat = feature_instance
    feat = feature_class(xr.Dataset.from_dict({
        'coords': {
            'lat': {
                'data': basefeat.dataset.lat.values,
                'dims': basefeat.dataset.lat.dims
            },
            'lon': {
                'data': basefeat.dataset.lon.values,
                'dims': basefeat.dataset.lon.dims
            },
            'time': {
                'data': basefeat.dataset.time.values,
                'dims': basefeat.dataset.time.dims
            }
        },
        'data_vars':{
            'my_var': {
                'data': basefeat.dataset['my_var'].values,
                'dims': basefeat.dataset['my_var'].dims
            }
        },
        'attrs': basefeat.dataset.attrs}))

    assert isinstance(feat, feature_class)


def test_create_feature_from_xarray(
        feature_class, feature_instance, instance_class):

    i_class_name = None
    if instance_class is not None:
        i_class_name = instance_class.__name__

    feat = feature_class(
        feature_instance.dataset, instance_class=i_class_name)

    assert isinstance(feat, feature_class)


def test_init_from_ncfile(input_file, feature_class, instance_class):
    dst = xr.open_dataset(input_file)

    i_class_name = None
    if instance_class is not None:
        i_class_name = instance_class.__name__

    feat = feature_class(dst, instance_class=i_class_name)

    assert isinstance(feat, feature_class)
    assert feat.dataset.cb.time_coverage_start is not None


def test_save_feature(feature_instance, output_file):
    feat = feature_instance
    feat.dataset.cb.save(path=output_file)


def test_get_lat(feature_instance):
    data = feature_instance.dataset['lat'].cb.to_masked_array()

    assert isinstance(data, np.ndarray)


def test_get_lon(feature_instance):
    data = feature_instance.dataset['lon'].cb.to_masked_array()

    assert isinstance(data, np.ndarray)


def test_get_times(feature_instance):
    data = feature_instance.dataset['time'].cb.to_masked_array()

    assert isinstance(data, np.ndarray)
    assert np.issubdtype(data.dtype, np.datetime64)


def test_get_values(feature_instance, test_var):
    feat = feature_instance
    data = feat.dataset[test_var].cb.to_masked_array()

    assert isinstance(data, np.ma.MaskedArray)


def test_get_geocoord(feature_instance):
    assert 'lat' in feature_instance.dataset.coords


def test_cf_dims(feature_instance, instance_class):
    """verify the expected dimensions for this feature are present"""
    dims = feature_instance.ds.cb.cf_dims

    # if feature_instance.featureType is None:
    #     return

    # if isinstance(feature_instance, BaseCollection):
    #     assert feature_instance.instance_class == instance_class
    #     cf_canonical_dims = feature_instance.instance_class.cf_canonical_dims
    # else:
    #     cf_canonical_dims = feature_instance.cf_canonical_dims
    cf_canonical_dims = feature_instance.cf_canonical_dims

    print(feature_instance.ds)
    print(feature_instance.ds.encoding)

    for var_type, c_dims in cf_canonical_dims.items():
        if var_type == 'data':
            continue

        coord = feature_instance.ds.cb.cf_axis_coords.get(var_type.upper())
        if coord is None:
            assert coord not in feature_instance.ds.cb.cf_coords
            continue

        # replace generic axes in v with actual name
        coord_dims = feature_instance.ds.cb.cfdataset[coord].dims
        c_dims = [feature_instance.ds.cb.cf_axis_dims.get(_, _) for _ in c_dims]

        assert (
            set(coord_dims) == set(c_dims) or
            set(coord_dims) == set(c_dims) - {feature_instance.cf_instance_axis}
        )


#
# def test_geodimnames(feature_instance, feature_dimnames):
#     dims = feature_instance.dataset.cb.geodimnames
#
#     assert isinstance(dims, tuple)
#     print(dims, feature_dimnames)
#     print(feature_instance)
#     #assert all([dims[i] == feature_dimnames[i] for i in range(len(dims))])
#     assert set(dims) == set(feature_dimnames)
#
#
# def test_geodimsizes(feature_instance, feature_dimsizes):
#     sizes = feature_instance.dataset.cb.geodimsizes
#
#     assert isinstance(sizes, tuple)
#     print(sizes)
#     print(feature_instance.dataset)
#     assert all([sizes[i] == feature_dimsizes[i] for i in range(len(sizes))])


def test_clone_field(input_file, feature_class, feature_instance, test_var):
    feat = feature_class(xr.open_dataset(input_file))
    cloned = feat.dataset[test_var].copy(deep=True)

    print(cloned)
    assert isinstance(cloned, xr.DataArray)

    feat2 = feat = feature_instance
    cloned2 = feat2.dataset[test_var].copy(deep=True)
    print(cloned2)
    assert isinstance(cloned2, xr.DataArray)
    assert cloned.name == cloned2.name


def test_guess_feature(input_file, feature_class):
    dst = xr.open_dataset(input_file)
    print(cerbere.guess_feature(dst), feature_class)
    assert cerbere.guess_feature(dst) == feature_class


def test_feature_iteration(feature_instance):
    if isinstance(feature_instance, BaseCollection):
        feature = feature_instance[0]
        assert isinstance(feature, feature_instance.instance_class)
