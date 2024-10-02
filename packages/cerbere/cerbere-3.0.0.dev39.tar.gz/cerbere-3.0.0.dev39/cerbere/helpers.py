from __future__ import annotations


from io import BufferedIOBase
from importlib_metadata import entry_points
import logging
import os
from pathlib import Path
import typing as T
import warnings

import numpy as np
import xarray as xr
from xarray.backends.common import AbstractDataStore

import cerbere.accessor.cdataarray
import cerbere.accessor.cdataset
import cerbere.cfconvention as cf
from .reader.basereader import BaseReader
from .feature.cbasefeature import BaseFeature
from .feature.cdiscretefeature import DiscreteFeature
from .feature.cbasecollection import BaseCollection


_datasets = {
        entry_point.name: entry_point
        for entry_point
        in entry_points().select(group='cerbere.plugins')
}

_readers = {
        entry_point.name: entry_point
        for entry_point
        in entry_points().select(group='cerbere.reader')
}

_features = {
        entry_point.name: entry_point
        for entry_point
        in entry_points().select(group='cerbere.features')
}

_feature = {
        entry_point.name: entry_point
        for entry_point
        in entry_points().select(group='cerbere.feature')
}



# Preserve the data dtype during masked array to xarray conversions (whe
# creating a DataArray from a numpy MaskedArray or from data with a
# _FillValue encoding attribute
_keep_dtype: bool = False


def set_options(keep_dtype: bool = True,
                longitude180: bool = True) -> None:
    """
    """
    global _keep_dtype, _longitude180
    _keep_dtype = keep_dtype
    _longitude180 = longitude180


def datasets():
    warnings.warn(
        'Usage of plugins is now deprecated and is replaced with xarray '
        'backend classes.', DeprecationWarning, stacklevel=2)
    return list(_datasets.keys())


def readers():
    return list(_readers.keys())


def _open_dataset(
        url: T.Union[str, Path],
        reader: BaseReader,
        **kwargs) -> xr.Dataset:
    """
    Open a file (netCDF, ZArr,...) and returns its content as a xarray_
    :class:`xarray.Dataset` object.
    """
    try:
        options = kwargs
        # for opt in ['mask_and_scale',
        #             'decode_cf',
        #             'decode_coords',
        #             'decode_times',
        #             'cache'
        #             ]:
        #     if opt not in options:
        #         options[opt] = True

        if isinstance(url, list):
            if 'combine' not in options:
                options['combine'] = 'by_coords'
            return reader.open_mfdataset(url, **options)
        else:
            return reader.open_dataset(url, **options)
    except IOError:
        logging.error('Could not read file: {}'.format(url))
        raise


def guess_reader_class(path) -> T.Type[BaseReader]:
    """Use the file patterns defined for each reader class to infer which
    reader class to use."""
    filename = Path(path).name

    candidates = []
    for rd in readers():
        # default reader : use only if no reader overrides this one
        if rd == 'xarray':
            continue
        tested_reader = _readers[rd].load()
        if tested_reader.guess_can_open(filename):
            candidates.append(tested_reader)

    if len(candidates) > 1:
        logging.warning(f'multiple readers matching this file pattern were '
                        f'found: {candidates}. Using the first of this list.')

    if len(candidates) > 0:
        return candidates[0]

    # defaults to xarray readers
    return BaseReader


def guess_feature(dataset: xr.Dataset) -> cerbere.feature.cfeature.BaseFeature:
    candidates = []
    for feat in _feature:
        feature_class = _feature[feat].load()
        match = feature_class.guess_feature(dataset)
        if match is not None:
            candidates.append(match)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        # group aliases
        aliases = {
            _: _.is_alias(dataset) for _ in candidates
            if _.is_alias(dataset) is not None}
        if len(aliases) == 1:
            if set(candidates) == \
                    set(aliases.keys()).union(set(aliases.values())):
                return list(aliases.keys())[0]
        logging.warning(
            f'Several features matching the dataset: {candidates}. Cerbere '
            f'can not decide unambiguously which one should be used and will '
            f'use: {candidates[0]}')
        return candidates[0]

    # raise Exception if no feature could be matched
    raise TypeError(
        'No feature class could be found matching this dataset. There may be '
        'to many non compliance to CF in this dataset and a reader class '
        'should be created to fix this.')


def as_feature(dataset: xr.Dataset) -> cerbere.feature.cfeature.BaseFeature:
    return guess_feature(dataset)(dataset)


def open_dataset(
        dataset: T.Union[str, Path],
        reader: T.Optional[str] = None,
        plugin: T.Optional[str] = None,
        **kwargs
        ):
    """
    Open a cerbere Dataset object.

    The following xarray options are always set to True by cerbere when
    opening a file:
    * mask_and_scale
    * decode_cf
    * decode_coords
    * decode_coords

    Args:
        dataset:  similar to ``dataset`` arg in Dataset base class
        plugin: Dataset class name
    """
    for option in ['mask_and_scale', 'decode_cf', 'decode_coords',
                   'decode_coords']:
        if option in kwargs:
            warnings.WarningMessage(
                f'option {option} is always set to True by cerbere. Your '
                f'argument setting for this option will be ignored.')

    # DEPRECATED - for compatibility with cerbere v2
    if plugin is not None:
        warnings.warn(
            'Usage of plugins is now deprecated and is replaced with xarray '
            'backend classes.', DeprecationWarning, stacklevel=2)
        try:
            # for compatibility with cerbere v2
            old_dataset_class = _datasets[plugin].load()
            engine = old_dataset_class.engine
        except KeyError:
            raise TypeError("Can't find plugin for: {}. Did you install it?"
                            .format(plugin))
        obj = _open_dataset(dataset, engine=engine, **kwargs)
        if obj is None:
            raise IOError('Dataset not correctly opened')

        # cerbere sets
        obj.cb.url = dataset

        return obj

    # Cerbere v3
    if reader is None:
        # try to guess which reader to use
        reader_class = guess_reader_class(dataset)
    else:
        reader_class = _readers[reader].load()
    if reader_class is not None:
        logging.debug(f'Reader class for this file: {reader_class}')

    obj = _open_dataset(
        dataset, reader=reader_class, **kwargs).pipe(
        reader_class.postprocess)
    if obj is None:
        raise IOError('Dataset not correctly opened')

    # cerbere sets
    obj.cb.url = dataset

    return obj.cb.cfdataset


def open_feature(
        filename_or_obj: str | os.PathLike[T.Any] | BufferedIOBase |
                         AbstractDataStore | xr.Dataset,
        feature: str = None,
        reader: str = None,
        **kwargs
        ) -> BaseFeature:
    """
    Open a cerbere Dataset into a feature object.

    Args:
        filename_or_obj: path to the file, as in Xarray ``open_dataset``
        feature: Feature class name. If None, cerbere will attempt to guess
            the feature class and return an object of this class
        reader: reader class name
    """
    if not isinstance(filename_or_obj, xr.Dataset):
        dst = cerbere.open_dataset(filename_or_obj, reader=reader, **kwargs)
    else:
        dst = filename_or_obj

    if feature is not None:
        return _feature[feature].load()(dst)

    # try to guess the feature
    guessed_feature = guess_feature(dst)
    if (issubclass(guessed_feature, BaseCollection) and
            guessed_feature.is_alias(dst) is None):
        instance_class = guessed_feature.infer_instance_class(dst)
        return guessed_feature(dst, instance_class=instance_class)
    return guessed_feature(dst)


def open_as_feature(
        feature: str,
        dataset: T.Union[str, Path] = None,
        plugin: str = 'Dataset',
        **kwargs
        ):
    """
    Open a cerbere Dataset into a feature object.

    Args:
        feature: Feature class name
        dataset:  similar to ``dataset`` arg in Dataset base class
        plugin: Dataset class name
    """
    warnings.warn(
        'Usage of Dataset classes is now deprecated and will be removed '
        'in cerbere 3.1+', DeprecationWarning, stacklevel=2)
    dataset = _datasets[plugin].load()(dataset, **kwargs)

    return _features[feature].load()(dataset)


def new_array(
        data: T.Any,
        name: T.Optional[T.Hashable] = None,
        science_dtype: T.Optional[T.Union[np.dtype, T.Type[float]]] = None,
        fill_value: T.Optional[T.Any] = None,
        precision: T.Optional[int] = None,
        long_name: T.Optional[str] = None,
        standard_name: T.Optional[T.Union[str, T.Tuple[str, str]]] = None,
        units: T.Optional[str] = None,
        ancillary_variables: T.Optional[T.List[str]] = None,
        set_longitude180: bool = True,
        **kwargs) -> xr.DataArray:
    """
    Creates a DataArray with cerbere properties.

    Creating a DataArray, even if not using the cerbere properties,
    helps to solve some shortcomings of xarray. In particular:
    * preserving the fill_value associated with MaskedArray
    * preserving the original science dtype (as xarray may change the
      array dtype during some operations.

    Args:
        dtype: the type of the data. Infer the type from the provided data by
            default. xarray changes the data type of arrays when using masking,
            defining the field true type with this keyword will ensure you
            always get the data in the expected dtype when accessing with
            `get_values` method. Data will also be saved with the expected
            dtype.

        precision (int, optional): number of significant digits (when writing
            the data on file)

        set_longitude180 (bool): set the longitude to be between -180/180 (
            longitudes between 0-360 will be modified when reading the
            coordinate)

        fields : the subfields composing the main field.
            This is intended to group for instance components of the same
            variable (such as a vector's northward and eastward components
            for wind, currents,...). This allows to relate these components
            to the same physical variable (e.g wind) and to a single
            qc_levels and qc_details information.

        fill_value : the default value to associate with missing data in the
            field's values. The fill value must be of the same type as
            `dtype`. If None, default fill value will be used
            unless `no_missing_value` is set.

        no_missing_value: if True, the field will not contain any missing value.
            In practice no _FillValue attribute will be written for this field
            when saving it. Use this for mask or flag fields for instance.

        units : the units in which the data are given (if
            applicable)

        description (str) : full name of the phenomenon. This corresponds
            to a long_name in attribute in a netCDF file.

        authority (str): naming authority referencing the provided
            standard name

        standard_name (optional, str): standard label for a phenomenon, with
            respect to the convention stated in `authority` argument.
            This corresponds to a standard_name attribute in a CF compliant
            NetCDF file.

        quality_vars: list of related quality fields
    """
    global _keep_dtype

    dtype = data.dtype

    if isinstance(data, xr.DataArray):
        array = data

    else:
        if isinstance(data, np.ma.MaskedArray):
            if fill_value is None:
                fill_value = data.dtype.type(data.fill_value)

            if _keep_dtype:
                data = data.filled(fill_value)

        array = xr.DataArray(data, **kwargs)

    if dtype != array.dtype:
        if _keep_dtype:
            raise ValueError("xarray tried to change the data dtype despite "
                             "the keep_dtype cerbere option is set.")

        # the data dtype was changed which is because the DataArray is
        # initialized from a numpy MaskedArray with actual masked data.
        # We need to ensure to keep all the information to reverse the
        # dtype conversion
        if not isinstance(data, np.ma.MaskedArray):
            raise TypeError('A MaskedArray is expected here... Check the '
                            'cerbere code, this must be a bug.')
        # ensure the information on the original dtype is preserved and there
        # is a fill_value defined
        if fill_value is None:
            # use same fill value as xarray would use
            fill_value = cf.default_fill_value(dtype)
        array.cb._cfarray.encoding['_FillValue'] = fill_value

    # standardize according to Cerbere CF and ACDD conventions
    array.cb.cerberize()

    if name is not None:
        array.name = name

    # ensure the information on the original dtype is preserved
    if science_dtype is not None:
        array.cb.science_dtype = science_dtype
    else:
        array.cb.science_dtype = dtype

    # fill value
    if fill_value is not None:
        array.cb.fill_value = fill_value

    if standard_name is not None:
        array.cb.standard_name = standard_name
    if long_name is not None:
        array.cb.description = long_name
    if precision is not None:
        array.cb.precision = precision
    if units is not None:
        array.cb.units = units
    if ancillary_variables is not None:
        array.cb.quality_vars = ancillary_variables

    if set_longitude180:
        array.cb.longitude180 = set_longitude180

    return array


def reader_class(name: str):
    return _readers[name].load()


def feature_class(name: str):
    return _feature[name].load()


def class_by_cf_feature_type(name: str) -> BaseFeature:
    """Return the feature class corresponding to a CF featureType attribute
    value"""
    for feat in _feature:
        feature_type = _feature[feat].load()
        if (issubclass(feature_type, DiscreteFeature) and
                feature_type.cf_feature_type is not None and
                feature_type.cf_feature_type.lower() == name.lower()):
            return feature_type
