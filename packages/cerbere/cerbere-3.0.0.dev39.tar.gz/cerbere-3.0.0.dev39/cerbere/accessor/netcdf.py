"""
Helper functions to save data to Cerbere CF / ACDD convention
"""
from datetime import datetime
import logging
from pathlib import Path
import typing as T

import pandas as pd
import shapely.geometry
import numpy as np
import xarray as xr

import cerbere.cfconvention as cf


def to_netcdf(
        path: T.Union[str, Path],
        dataset: xr.Dataset,
        profile: str = 'default_saving_profile.yaml',
        force_profile: bool = False,
        keep_src_encoding: bool = False,
        **kwargs):
    """
    Save a dataset as CF compliant netCDF file

    Args:
        path:
        dataset:
        profile (str, optional): path to a specific format profile to
            apply before saving (or default formatting profile is used).
        force_profile (bool, optional): force profile attribute values to
            supersede existing ones in dataset attributes.
        keep_src_encoding (bool): keep original dtype, _FillValue
            and scaling if any (through `add_offset` or `scale_factor`
            attributes) as in the source data.

    Returns:

    """
    if 'format' in kwargs and 'NETCDF' not in kwargs['format']:
        raise ValueError(f'Unknown output format : {kwargs["format"]}')

    # saved version of the dataset
    dataset = dataset.copy(deep=False)

    # clear previous formatting rules
    if not keep_src_encoding:
        for v in dataset.variables:
            for attr in ['dtype', 'scale_factor', 'add_offset']:
                if attr in dataset[v].encoding:
                    dataset[v].encoding.pop(attr)

    # apply new formatting rules
    saved_dataset = _convert_format(dataset,
        profile=profile, force_profile=force_profile)

    # ensure proper type in output attributes so that it does not
    # generate errors for types not managed by the NetCDF lib
    _format_attrs_for_nc(saved_dataset)

    def has_scaling(variable: str):
        acc = dataset[variable].cb
        return acc.scale_factor is not None or acc.add_offset is not None

    # ensure original or overriding encoding
    for v in saved_dataset.variables:
        svar = saved_dataset[v]
        if keep_src_encoding:
            encoding = dataset.cb._orig_dataset[v].encoding
        else:
            encoding = svar.encoding

        if 'zlib' not in encoding:
            encoding['zlib'] = True
        if 'complevel' not in encoding:
            encoding['complevel'] = 4

        # save a _FillValue matching the encoding data type
        if 'grid_mapping_name' not in svar.attrs:
            encoding['_FillValue'] = encoding.get(
                '_FillValue', svar.attrs.get('_FillValue'))
        else:
            if '_FillValue' in encoding:
                encoding.pop('_FillValue')

        if np.issubdtype(svar.dtype, np.datetime64) \
                and svar.cb.units is None:
            svar.cb.units = cf.DEFAULT_TIME_UNITS

        if (np.issubdtype(svar.dtype, np.datetime64)
                or np.issubdtype(svar.dtype, np.timedelta64)):
            dtype = np.dtype(np.float64)
        else:
            dtype = encoding.get('dtype', svar.dtype)
        encoding['dtype'] = dtype

        # adjust missing value attribute types if packing is applied
        for matt in ['valid_min', 'valid_max', 'valid_range']:
            if matt in svar.attrs:
                svar.attrs[matt] = np.array(
                    svar.attrs[matt],
                    dtype=dtype)

        saved_dataset[v].encoding = encoding

        if np.issubdtype(saved_dataset[v].dtype, np.datetime64):
            # _FillValue can not be NaT or netcdf writing will fail
            if pd.isnull(saved_dataset[v].encoding['_FillValue']):
                saved_dataset[v].encoding['_FillValue'] = 1e20

            # units must be in encoding
            if 'units' in saved_dataset[v].attrs:
                saved_dataset[v].encoding['units'] = saved_dataset[
                    v].attrs.pop('units')

    saved_dataset.to_netcdf(
        path=path,
        engine='h5netcdf',
        **kwargs
    )


def _add_global_attrs(
        dataset: xr.Dataset,
        attrs: T.Mapping[str, T.Any],
        force_profile: bool = False) -> None:
    """Add default attributes to the dataset from a attribute definition
    file.

    Used when formatting with a template.

    Args:
        attrs (dict): the global attributes to add when saving the dataset
    """
    # add attributes
    # don't override previous attribute values
    for att in attrs:
        if att not in dataset.attrs or force_profile:
            if attrs[att] is None:
                continue
            dataset.attrs[att] = attrs[att]


def _add_var_attrs(
        dataset: xr.Dataset,
        attrs: T.Mapping[str, T.Any],
        force_profile: bool = False) -> None:
    """Add field attributes to the dataset from a attribute definition
    file.

    Used when formatting with a template.

    Args:
        attrs (dict): the field attributes to add when saving the dataset
    """
    # add attributes
    # don't override previous attribute values
    for v in attrs:
        if v not in dataset.variables:
            logging.warning(
                f'Variable {v} not found in the dataset to save. Skipping')
            continue

        for att in attrs[v]:
            if att not in dataset.variables[v].attrs or force_profile:
                value = attrs[v][att]
                if value is None:
                    continue
                dataset.variables[v].attrs[att] = value


def _add_var_encoding(
        dataset: xr.Dataset,
        attrs: T.Mapping[str, T.Any],
        force_profile: bool = False) -> None:
    """Add field encoding to the dataset from a attribute definition
    file.

    Used when formatting with a template.

    Args:
        attrs (dict): the field encoding attributes to add when saving the
            dataset
    """
    # add attributes
    # overrides previous attribute values!!
    for v in attrs:
        if v not in dataset.variables:
            logging.warning(
                f'Variable {v} not found in the dataset to save. Skipping')
            continue

        if attrs[v] is None:
            continue

        for att in attrs[v]:
            if att not in dataset.variables[v].encoding or force_profile:
                value = attrs[v][att]
                if value is None:
                    continue
                dataset.variables[v].encoding[att] = value


def _convert_format(cfdataset, profile=None, force_profile=False, **kwargs):
    """Implement specific formatting rules to a dataset.

    Used before saving the dataset to match some specific format
    requirements when writing the dataset on file.

    A custom format profile can be provided, using ``profile``
    argument, otherwise the default cerbere profile will be used.

    Refer to :func:`~cerbere.cfconvention.default_profile`
    """
    dataset = cfdataset.copy()

    # read custom settings for the dataset saving
    gattrs, vattrs, encoding = cf.default_profile(profile=profile)

    # add global attributes from custom settings
    _add_global_attrs(dataset, gattrs, force_profile=force_profile)

    # add field attributes from custom settings
    _add_var_attrs(dataset, vattrs, force_profile=force_profile)

    # add field encoding from custom settings
    _add_var_encoding(dataset, encoding, force_profile=force_profile)

    return dataset


def _format_attrs_for_nc(dataset):
    """format the attributes in an acceptable type for netCDF"""
    # global attrs
    invalid_attrs = []
    for att in dataset.attrs:
        # remove None attributes
        if dataset.attrs[att] is None:
            invalid_attrs.append(att)
            continue
        # convert datetime objects to string
        dataset.attrs[att] = _format_attr(dataset.attrs[att])
    for att in invalid_attrs:
        dataset.attrs.pop(att)

    # variable attrs
    for varname in dataset._variables:
        var = dataset._variables[varname]
        invalid_attrs = []
        for att in var.attrs:
            if var.attrs[att] is None:
                invalid_attrs.append(att)
                continue

            if att == '_FillValue':
                # should be in encoding
                if '_FillValue' in var.encoding:
                    raise ValueError(f'two fill values defined for {varname}')
                var.encoding[att] = var.attrs.pop(att)

        for att in invalid_attrs:
            var.attrs.pop(att)


def _format_attr(attrval):
    if isinstance(attrval, datetime):
        return attrval.strftime(cf.FORMAT_TIME)
    elif attrval is None:
        return ''
    elif isinstance(attrval, shapely.geometry.base.BaseGeometry):
        return attrval.wkt
    return attrval