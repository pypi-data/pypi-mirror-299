"""
Base classes for cerbere dataset objects and to read/save datasets in different
file formats and conventions.

.. autosummary::
    :toctree: _autosummary

    field
    dataset
    ncdataset
    ghrsstncdataset
"""
import logging
from enum import Enum
from typing import Union

import numpy as np
import xarray as xr

# cerbere internals for encoding/decoding data to file or memory
ENCODING = 'cerbere'


class Encoding(Enum):
    """attributes for saving the encoding of a source file"""

    # source file's saved encoding attributes
    IO_FILLVALUE: str = 'io__FillValue'
    IO_SCALE: str = 'io_scale_factor'
    IO_OFFSET: str = 'io_add_offset'
    IO_DTYPE: str = 'io_dtype'

    # in memory numpy encoding
    M_DTYPE: str = 'm_dype'
    M_MASK: Union[np.ndarray, bool] = 'mask'

    # individual components for vectorial fields
    COMPONENTS: str = 'components'

    # field status wrt to its copy on file
    STATUS: str = 'status'


def default_fill_value(obj):
    """Returns the default fill value for a specific type"""
    if isinstance(obj, np.dtype):
        dtype = obj
    elif isinstance(obj, (str, type)):
        dtype = np.dtype(obj)
    elif isinstance(obj, np.ndarray):
        dtype = obj.dtype
    else:
        raise TypeError('Unexpected object type: ', type(obj), obj)

    if dtype.name == 'int16':
        return np.int16(-32768)
    elif dtype.name == 'uint16':
        return np.uint16(65535)
    elif dtype.name == 'int8':
        return np.int8(-128)
    elif dtype.name == 'uint8':
        return np.uint8(255)
    elif dtype.name == 'float32':
        return np.float32(np.ma.default_fill_value(dtype))
    elif dtype.name == 'float64':
        return np.float64(np.ma.default_fill_value(dtype))
    else:
        return np.ma.default_fill_value(dtype)


def infer_fillvalue(fill_value, data, dtype):
    if fill_value is not None:
        return fill_value

    # use valid xarray missing values if possible (float or datetime64)
    if np.issubdtype(data.dtype, np.floating) or \
            np.issubdtype(data.dtype, np.complexfloating):
        fill_value = np.nan
    elif np.issubdtype(dtype, np.datetime64):
        fill_value = np.datetime64('NaT')
    else:
        try:
            fill_value = data.fill_value
        except:
            fill_value = default_fill_value(dtype)

    return fill_value

def to_cerbere_dataarray(
        data: Union[xr.DataArray, np.ndarray, np.ma.MaskedArray],
        fill_value: float = None,
        dtype: np.dtype = None,
        no_missing_value: bool = False,
        **kwargs) -> xr.DataArray:
    """Converts to a cerbere DataArray.

    A cerbere DataArray adds specific internal attributes into the
    `encoding` property of a DataArray, such as:
      * the mask of missing values (like for a numpy MaskedArray),
        which is not supported by DataArray (which replaces masked values
        with NaN)
      * the scientific dtype of the data (which may be different for the in
        memory encoding since xarray will transform the dtype of MaskedArray
        into floats.

    Used for internal data encoding as xarray data can't store masked
    values or nan for non-float types and transforms masked arrays to float
    arrays, which leads to a changed dtype of an array. When using cerbere
    `get_values` method, the data returned to the users will be in the
    internal DataArray dtype (with NaN for fill values when any), unless
    `decoding` keyword is set to True (NaN are then replaced be the fill_value
    attribute and the dtype of the returned values is the scientific one). The
    mask can be retrieved with the `mask` property of a Field object.

    Args:
        data: Array to be converted to masked DataArray
        fill_value: Fill value. Must be of the same type as dtype
        dtype: array's scientific data type. It can be different
            from `dtype` of `data` array. Data returned with `get_values`
            will be forced to this type.
        **kwargs: other DataArray creation arguments
    """
    if dtype is None:
        dtype = data.dtype

    if dtype != data.dtype:
        logging.debug('Data internally stored as {} but tht scientific dtype '
                      'is {}'.format(data.dtype, dtype))

    if no_missing_value and fill_value is not None:
        raise ValueError('no_missing_value is set to True but a fill_value was '
                         'also provided')

    if fill_value is None and data.dtype != dtype:
        # There is no reason here for xarray to have a different data type
        # than the scientific one.
        logging.warning('internal data type {} should be the same than '
                        'scientific data type {}'.format(data.dtype, dtype))

    if isinstance(data, np.ma.core.MaskedArray):
        if no_missing_value:
            if data.count() != data.size:
                raise ValueError('no_missing_value set to True but data '
                                 'contains masked values')
            logging.warning('data was provided as a masked array with '
                            'no_missing_value set to True. data will be '
                            'forced to non masked array.')
            mask = None
        else:
            mask = data.mask
    else:
        # mask - case ndarray, Dask array DataArray
        try:
            # numpy array type
            mask = np.isnan(data) | (data == fill_value)
        except:
            # xarray array type
            mask = data.isnull() | (data == fill_value)
        if np.all(mask):
            mask = True
        elif np.all(~mask):
            mask = False
            if fill_value is None:
                # no explicit fill values, no nan in data : this is a unmasked
                # variable
                mask = None

    # wrap into xarray DataArray
    data = xr.DataArray(data=data, **kwargs)

    if ENCODING not in data.encoding:
        data.encoding[ENCODING] = {}
    data.encoding[ENCODING][Encoding.M_DTYPE] = dtype

    # no mask in the variable
    data.encoding[ENCODING][Encoding.M_MASK] = mask

    # ensure there is a defined fill value
    if mask is not None:
        data.encoding['_FillValue'] = infer_fillvalue(
            fill_value, data, dtype)

    return data


def io_encoding_dtype(data: xr.DataArray) -> np.dtype:
    """guess the scientific dtype from data read on file"""
    scale = data.encoding.get(
        'scale_factor', data.encoding.get('add_offset', None))
    fillv = data.encoding.get(
        '_FillValue', data.attrs.get('_FillValue', None))
    if scale is None:
        # no scaling of data -> dtype should be unchanged

        if fillv is None:
            return data.dtype

        if np.dtype(type(fillv)) != data.dtype and not np.issubdtype(
                data.dtype, np.datetime64):
            # no scaling was applied but xarray may have changed the dtype for
            # instance if fill values were replaced with NaN. Returns the
            # intended scientific dtype indicated by the _FillValue attr.
            return np.dtype(type(fillv))

        return data.dtype

    else:
        dtype = np.dtype(type(scale))
        if dtype != data.dtype:
            # xarray may have changed the dtype for instance if fill values
            # were replaced with NaN. Returns the intended scientific dtype
            # indicated by the scaling attributes
            return dtype

    return dtype


def from_cerbere_dataarray(
        data,
        as_masked_array: bool = True,
        decoding: bool = False) -> Union[xr.DataArray, np.ma.MaskedArray]:
    """"""
    if not isinstance(data, xr.DataArray):
        raise TypeError('unexpected data type: {}'.format(type(data)))

    fillv = data.encoding.get('_FillValue', data.attrs.get(
        '_FillValue', None))

    if ENCODING not in data.encoding or \
            Encoding.M_DTYPE not in data.encoding[ENCODING]:
        # the data were not yet internally encoded or were read from an
        # externally defined DataArray or from a file => us the native encoding
        if as_masked_array:
            dtype = io_encoding_dtype(data)
            data = data.astype(dtype, copy=False).to_masked_array(copy=False)
            data.set_fill_value(fillv)
        elif decoding:
            dtype = io_encoding_dtype(data)
            data = data.astype(dtype, copy=False)

        return data

    if decoding and not as_masked_array:
        # return the data in their scientific dtype, replacing NaN with fill
        # values
        return data.fillna(data.encoding['_FillValue']).astype(
            data.encoding[ENCODING][Encoding.M_DTYPE], copy=False)

    if as_masked_array:
        mdata = data.astype(
            data.encoding[ENCODING][Encoding.M_DTYPE],
            copy=False).to_masked_array(copy=False)

        if Encoding.M_MASK in data.encoding[ENCODING]:
            mask = data.encoding[ENCODING][Encoding.M_MASK]
            if mask is not None:
                mdata = np.ma.masked_where(mask, data)
        else:
            mdata.mask = np.where(mdata == fillv)

        mdata.set_fill_value(fillv)

        return mdata

    # return the data in their internal dtype
    return data
