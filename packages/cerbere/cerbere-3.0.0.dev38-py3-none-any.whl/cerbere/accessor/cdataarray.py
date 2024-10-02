# -*- coding: utf-8 -*-
"""
Classes for the handling the fields.
"""
import collections
import inspect
import logging
import typing as T

try:
    # python >= 3.7.2
    from typing import OrderedDict
except ImportError:
    # python >= 3.6
    from typing import MutableMapping as OrderedDict

import warnings

import numpy as np
from scipy.ndimage import find_objects, label, binary_dilation
import shapely.geometry
import xarray as xr
from xarray.core.utils import either_dict_or_kwargs
from xarray.core.dataarray import _LocIndexer

import cerbere.cfconvention as cf

T_Coverage = T.Literal[
    'image', 'thematicClassification', 'physicalMeasurement',
    'auxiliaryInformation', 'qualityInformation', 'referenceInformation',
    'modelResult', 'coordinate'
]


FIELD_ATTRS = [
    'standard_name',
    'authority',
    'units',
    'valid_min',
    'valid_max',
    '_FillValue'
]
FIELD_EXCL_ATTRS = [
    'long_name'
]


def _has_nonfinite(x):
    if np.issubdtype(x.dtype, np.dtype(np.datetime64)):
        return np.isnat(np.asarray(x).sum())
    elif (np.issubdtype(x.dtype, np.dtype('O'))
              or np.issubdtype(x.dtype, np.dtype('U'))):
        return True
    return np.isnan(np.asarray(x).sum())


class _CLocIndexer(_LocIndexer):

    def __getitem__(self, key) -> xr.DataArray:
        return super().__getitem__(key)

    def __setitem__(self, key, value) -> None:
        if _has_nonfinite(value):
            if self.data_array.cb.fill_value is None:
                # masked value are set on a data array which had no fill value
                # xarray will create a default fill value but without filling
                # in the encoding attribute; we fix that.
                self.data_array.cb._cfarray.encoding['_FillValue'] = \
                    cf.default_fill_value(
                        self.data_array.cb.science_dtype)

        self.data_array.loc[key] = value


@xr.register_dataarray_accessor("cb")
class DataArrayAccessor:
    """Describes a scientific data array. It contains data and
    metadata attributes.

    This is an extension of xarray's DataArray with stricter requirements on
    attributes and the encoding of masked arrays.
    """
    def __init__(self, xarray_obj):
        self._orig_array = None

        self._cfarray = xarray_obj
        self.is_cerberized: bool = False

        self.longitude180: bool = True

        self.cerberize()

    @property
    def cfarray(self) -> xr.DataArray:
        """Returns a CF normalized version of the dataset."""
        if self._cfarray is None:
            # default standardization - may not be enough for some products
            # that have more unusual none-conformity
            self.cerberize()

        return self._cfarray

    def cerberize(self):
        """
        Do whatever is necessary to make the variable compliant to Cerbere
        conventions (based on CF, ACDD).

        May not be enough for some products that have more unusual
        none-conformity.
        """
        if self.is_cerberized:
            # already cerberized
            return

        # back-up original version for encoding information - NOTE: the
        # modified array has to be the array of of the accessor or strange
        # behaviour may occur (like with loc function).
        # @TODO may have a memory imprint if some data copy occur - may be
        #  better to only save variable and global encoding
        self._orig_array = self._cfarray.copy(deep=False)

        # guess science data type
        self._cfarray.encoding['science_dtype'] = self._guess_science_dtype()

        # fix some possible mismatch between the science data dtype and the
        # fill value dtype
        self._fix_fill_value()

        self.is_cerberized = True

    def _fix_fill_value(self) -> None:
        """Fix the data fill value if its dtype is mismatching the
        science data dtype.

        Cases where such mismatch may occur:

        * data are read from a file which uses scaling (through `scale_factor`
          and `add_offset` CF attributes). The _FillValue is given for the
          storage type (which may be an integer even if the data are unscaled to
          a float type.
        * xarray creates automatically some _FillValue in its encoding
          attribute (for instance when setting np.nan in the data): for
          floating values, the created _FillValue may be a float64 instead of a
          float32 when float32 is the actual data dtype.
        """
        # enforce fill value for datetime64 and timedelta64 arrays
        if np.issubdtype(self.cfarray.encoding['science_dtype'],
                         np.datetime64):
            self.cfarray.encoding['_FillValue'] = np.datetime64('NaT')
            return
        if np.issubdtype(self.cfarray.encoding['science_dtype'],
                         np.timedelta64):
            self.cfarray.encoding['_FillValue'] = np.timedelta64('NaT')
            return

        # @ TODO : check before uncommenting -> conflict with following code
        # if ('_FillValue' not in self.cfarray.encoding and '_FillValue' not in
        #         self.cfarray.attrs):
        #     return

        # xarray sometimes holds _FillValue in attrs...
        fv = self.cfarray.encoding.get(
            '_FillValue', self.cfarray.attrs.get('_FillValue'))

        if fv is None and _has_nonfinite(self.cfarray):
            # if the array has none-finite values, it must have a fill value
            # different from None => affect one
            fv = cf.default_fill_value(self.cfarray.encoding['science_dtype'])
            self.cfarray.encoding['_FillValue'] = fv

        if fv is None:
            return

        data_dtype = self.cfarray.encoding['science_dtype']

        # data_dtype = self.cfarray.dtype
        fv_dtype = np.dtype(type(fv))

        if data_dtype != fv_dtype:
            # force the _FillValue to same as science data dtype
            self.cfarray.encoding['_FillValue'] = data_dtype.type(
                self.cfarray.encoding['_FillValue'])

        # if np.issubdtype(data_dtype, np.floating) and \
        #         np.issubdtype(fv_dtype, np.floating):
        #     # fix the _FillValue
        #     self.cfarray.encoding['_FillValue'] = cf.default_fill_value(
        #         data_dtype)


        # fv_dtype = None
        # if self.cfarray.encoding.get('_FillValue') is not None:
        #     fv_dtype = np.dtype(type(self.cfarray.encoding.get('_FillValue')))
        # if len(encoding_dtype) == 0 and fv_dtype is not None:
        #     # no data scaling: verify the _FillValue is consistent with the
        #     # data dtype as xarray creates automatically some _FillValue in
        #     # encoding attribute (for instance when setting np.nan in the data)
        #     # for floating values, the created _FillValue may be a float64
        #     # instead of a float32
        #     if np.issubdtype(self.cfarray.dtype, np.floating) and \
        #             np.issubdtype(fv_dtype, np.floating):
        #         # fix the _FillValue
        #         self.cfarray.encoding['_FillValue'] = cf.default_fill_value(
        #             self.cfarray.dtype)
        #         fv_dtype = self.cfarray.dtype
        #     encoding_dtype = {fv_dtype}
        # elif fv_dtype is not None:
        #     encoding_dtype = encoding_dtype.union({fv_dtype})

    def _guess_science_dtype(self) -> np.dtype:
        """
        Guess the scientific dtype from data read on file.

        xarray sometimes transform a DataArray dtype, for instance when
        converting fill values from a numpy MaskedArray to NaN which are only
        defined for floating types. Integer, bytes, etc... array can then be
        converted to float. This happens for instance when reading masked
        integer variables from a NetCDF file.

        In cerbere we keep track of the "true" scientific dtype to return for
        instance numpy ndarray or MaskedArray objects in their true
        original dtype.
        """
        if 'science_dtype' in self._cfarray.encoding:
            return self._cfarray.encoding['science_dtype']

        if np.issubdtype(self._cfarray.dtype, np.datetime64):
            # ignore internal dtype encoding
            return self._cfarray.dtype

        # if data are read from a file, the scaling CF attributes,
        # if present, give the scientific data dtype
        encoding_dtype = {np.dtype(type(_)) for _ in [
            self._cfarray.encoding.get('scale_factor'),
            self._cfarray.encoding.get('add_offset')]
            if _ is not None
        }

        if len(encoding_dtype) == 0:
            # no encoding : assume the array dtype is the same as the
            # scientific dtype
            return self._cfarray.dtype

        if len(encoding_dtype) == 1:
            # all encoding scaling attributes are consistent
            return next(iter(encoding_dtype))

        if len(encoding_dtype) > 1:
            dtypes = {
                _: np.dtype(type(self._cfarray.encoding[_]))
                for _ in ['scale_factor', 'add_offset']
                if _ in self._cfarray.encoding
            }
            logging.warning(
                f'inconsistent dtypes in CF encoding attributes: {dtypes}. '
                f'This should be fixed by the producer of these data.')

            # assuming the scale factor is more correct
            return dtypes['scale_factor']

    @property
    def fill_value(self) -> T.Union[T.Any, None]:
        """The value for missing data in the field"""
        return self.cfarray.encoding.get('_FillValue')

    @fill_value.setter
    def fill_value(self, fill_value: T.Any):
        """set the value for missing data"""
        if fill_value is None:
            # @TODO : raise exception if any masked value ?
            self.cfarray.encoding['_FillValue'] = None
            return

        # do some checks on consistency with data type
        if self.science_dtype is not None and not np.issubdtype(
                np.dtype(type(fill_value)), self.science_dtype):
            raise TypeError(
                f'the dtype {np.dtype(type(fill_value))} for the fill_value '
                f'is not consistent with data dtype {self.science_dtype}')

        if self.cfarray.cb.fill_value is None:
            self.cfarray.encoding['_FillValue'] = fill_value
            return

        if self.cfarray.cb.fill_value != fill_value:
            # a fill value is already set and different from the new one,
            # the existing masked values need to be replaced
            logging.warning(
                f'Changing the fill values in array {self.cfarray.name} from '
                f'{self.cfarray.cb.fill_value} to {fill_value}. This '
                f'should be avoided for memory and performance issues.')
            self._cfarray = self._replace_fill_value(
                self.cfarray, self.cfarray.cb.fill_value, fill_value)

        self.cfarray.encoding['_FillValue'] = fill_value

    @property
    def precision(self) -> T.Union[int, None]:
        """The least significant digit for the values of the field.

        Used for storage optimization when writing on disk. The least
        significant digit is the power of ten of the smallest decimal place in
        the data that is a reliable value.
        """
        return self.cfarray.encoding.get('least_significant_digit')

    @precision.setter
    def precision(self, precision: int):
        """Set the least significant digit for the values of the field.

        Used for storage optimization when writing on disk. The least
        significant digit is the power of ten of the smallest decimal place in
        the data that is a reliable value.
        """
        self.cfarray.encoding['least_significant_digit'] = precision

    @property
    def valid_min(self) -> T.Union[T.Any, None]:
        """The minimum valid value in the field data"""
        return self.cfarray.attrs.get('valid_min')

    @valid_min.setter
    def valid_min(self, value: T.Any):
        """set the minimum valid value (``valid_min`` CF attribute)"""
        self.cfarray.attrs['valid_min'] = value

    @property
    def valid_max(self) -> T.Union[T.Any, None]:
        """The maximum valid value in the data (``valid_max`` CF attribute)"""
        return self.cfarray.attrs.get('valid_max')

    @valid_max.setter
    def valid_max(self, value: T.Any):
        """set the maximum valid value (``valid_max`` CF attribute)"""
        self.cfarray.attrs['valid_max'] = value

    @property
    def scale_factor(self) -> T.Union[T.Any, None]:
        """The encoding scaling factor for the data (``scale_factor`` CF
        attribute)"""
        return self.cfarray.encoding.get('scale_factor')

    @scale_factor.setter
    def scale_factor(self, value: T.Any):
        """set the encoding scaling factor (``scale_factor`` CF attribute)"""
        self.cfarray.encoding['scale_factor'] = value

    @property
    def add_offset(self) -> T.Union[T.Any, None]:
        """The encoding offset factor for the data (``add_offset`` CF
        attribute)"""
        return self.cfarray.encoding.get('add_offset')

    @add_offset.setter
    def add_offset(self, value: T.Any):
        """set the encoding offset factor (``scale_factor`` CF attribute)"""
        self.cfarray.encoding['add_offset'] = value

    @property
    def axis(self) -> T.Optional[str]:
        """The spatiotemporal axis represented by this variable (
        ``axis`` CF attribute). None if is not set as an axis."""
        return self.cfarray.attrs.get('axis')

    @property
    def units(self) -> T.Union[str, None]:
        """The variable data units (``units`` CF attribute)"""
        return self.cfarray.encoding.get(
            'units', self.cfarray.attrs.get('units'))

    @units.setter
    def units(self, units: str):
        """Set the variable data units (``units`` CF attribute)"""
        if 'units' in self.cfarray.encoding:
            self.cfarray.encoding['units'] = units
        else:
            self.cfarray.attrs['units'] = units

    @property
    def long_name(self) -> T.Union[str, None]:
        """The variable description (``long_name`` CF attribute)"""
        return self.cfarray.attrs.get('long_name')

    @long_name.setter
    def long_name(self, long_name: str) -> None:
        """set the variable description (``long_name`` CF attribute)"""
        self.cfarray.attrs['long_name'] = long_name

    @property
    def standard_name(self) -> T.Union[str, None]:
        """The variable standard name (``standard_name`` CF attribute)"""
        return self.cfarray.attrs.get('standard_name')

    @standard_name.setter
    def standard_name(self, standard_name: str) -> None:
        """set the standard_name (``standard_name`` CF attribute)"""
        self.cfarray.attrs['standard_name'] = standard_name

    @property
    def ancillary_variables(self):
        """CF Attribute: identifies a variable that contains closely
        associated data, e.g., the measurement uncertainties of instrument data.
        """
        return self.cfarray.attrs['ancillary_variables']

    @ancillary_variables.setter
    def ancillary_variables(self, value: T.List[str]):
        self.cfarray.attrs['ancillary_variables'] = value

    @property
    def coverage_content_type(self) -> T.Union[T_Coverage, None]:
        """ACDD 1.3 attribute; An ISO 19115-1 code to indicate the source of the
        data (image, thematicClassification, physicalMeasurement,
        auxiliaryInformation, qualityInformation, referenceInformation,
        modelResult, or coordinate).
        """
        return self.cfarray.attrs['coverage_content_type']

    @coverage_content_type.setter
    def coverage_content_type(self, value: T_Coverage):
        if value not in cf.COVERAGE_CONTENT_TYPE:
            raise ValueError(
                f'value {value} is not allowed. It should be one of the '
                f'following: {list(cf.COVERAGE_CONTENT_TYPE)}')
        self.cfarray.attrs['coverage_content_type'] = value

    @property
    def science_dtype(self) -> np.dtype:
        """The scientific dtype of the data (ignores xarray
        internal conversion)"""
        if self.cfarray.encoding.get('science_dtype') is None:
            self.cfarray.encoding['science_dtype'] = self._guess_science_dtype()
        return self.cfarray.encoding['science_dtype']

    @science_dtype.setter
    def science_dtype(self, value: np.dtype):
        if not isinstance(np.dtype(value), np.dtype):
            raise TypeError(f'{value} is not a numpy dtype')
        self.cfarray.encoding['science_dtype'] = np.dtype(value)

    def __str__(self):
        result = "\nField : '%s'\n" % self.cfarray.name
        if ('long_name' in self.cfarray.attrs and
                self.cfarray.attrs['long_name'] is not None):
            result += '    {}\n'.format(self.cfarray.attrs['long_name'])
        result += '\n'

        # dimensions
        result = result + '    dimensions :\n'
        dims = collections.OrderedDict(self.cfarray.sizes.items())
        for dim, size in dims.items():
            result += '      # {} : {}\n'.format(dim, size)

        attrs = self.cfarray.attrs.items()

        # standard attributes
        result = result + '    standard CF attributes :\n'
        for att, val in attrs:
            if att in FIELD_ATTRS:
                result += '      # {} : {}\n'.format(att, val)
        result += '      # fill_value : {}\n'.format(str(self.fill_value))

        # free form attributes
        result = result + '    other attributes :\n'
        for att, val in attrs:
            if att not in FIELD_ATTRS and att not in FIELD_EXCL_ATTRS:
                result = result + '      # {} : {}\n'.format(att, val)

        return result

    def is_axis(self, axis: str) -> bool:
        """Returns true if the field is the coordinate field for the given axis.

        Args:
            axis: axis name (among X, Y, Z, T)
        """

    def _broadcast_coords(
            self,
            values: xr.DataArray,
            broadcast_coords: T.List[xr.DataArray]):
        """
        Broadcast the values along a list of existing and new coordinates.

        Existing coordinates are ignored, except for ordering the dimensions
        in the output array (following the order given in broadcast_coords).
        If existing coordinates of the array are not listed in
        broadcast_coords, they follow the ones given in broadcast_coords in
        the order of the dimensions of the output array.

        Args:
            coords: coordinates along which to broadcast

        Returns:

        """
        # brodcast values over the requested dimensions
        cdims = [_.name for _ in broadcast_coords]
        for coord in broadcast_coords[::-1]:
            dim = coord.name
            if dim in self._cfarray.dims:
                # this coordinate is already a coordinate of the current array:
                # no broadcasting needed
                continue

            values = values.broadcast_like(coord)

        # # @TODO check more cases
        # squeezed_dims = [
        #     # _ for _ in self.dims
        #     _ for _ in self._cfarray.dims
        #     if _ in self.geocoordnames and _ not in broadcast_coords
        # ]
        # values = values.squeeze(dim=squeezed_dims, drop=True)
        # rearranged_dims = cdims + [
        #     _ for _ in values.dims if _ not in cdims
        # ]
        #
        # re-order dims
        # if len(values.dims) > 0 & (values.dims != rearranged_dims):
        #     values = values.transpose(
        #         *(list(rearranged_dims)), transpose_coords=True)
        rearranged_dims = cdims + [
             _ for _ in values.dims if _ not in cdims
        ]
        if len(values.dims) > 0 & (values.dims != rearranged_dims):
            values = values.transpose(
                *(list(rearranged_dims)), transpose_coords=True)

        return values

    def broadcast(self,
                  target: T.Union[
                      xr.DataArray,
                      T.List[T.Union[xr.DataArray, str]]],
                  feature = None):
        """Broadcast the values of a DataArray along the coordinates of
        another DataArray or a list of coordinates.
        """
        if isinstance(target, xr.DataArray):
            return self._cfarray.broadcast_like(target)
        elif isinstance(target, list):
            if len(target) == 0:
                raise ValueError('Cannot broadcast along an empty list of '
                                 'coordinates')
            if isinstance(target[0], xr.DataArray):
                return self._broadcast_coords(self._cfarray, target)
            elif isinstance(target[0], str):
                if feature is None:
                    raise ValueError(
                        'feature object must be provided when broadcasting by '
                        'coordinate names')
                return self._broadcast_coords(
                    self._cfarray, [feature.ds[_] for _ in target])

        raise TypeError('target type not accepted for broadcast operation')

    def isel(
            self,
            indexers = None,
            padding: bool = False,
            broadcast_coords: T.List[xr.DataArray] = None,
            as_science_dtype: bool = False,
            as_masked_array: bool = False,
            **kwargs: T.Any):
        """

        Args:
            padding: pad the result with fill values where slices are out of the
                field dimension limits. Default is False.
            as_science_dtype: returns the data in their science dtype,
                replacing NaN with fill values
            **kwargs:

        Returns:

        """
        # separate indexer kargs from isel other kwargs
        # remove dims of indexer not in the variable
        isel_signature = inspect.getfullargspec(self.cfarray.isel).args
        isel_kwargs = {k: v for k, v in kwargs.items() if k in isel_signature}
        indx_kwargs = {k: v for k, v in kwargs.items() if k not in
            isel_signature}
        sel = either_dict_or_kwargs(indexers, indx_kwargs, "isel")

        if padding:
            sel = {
                dim: slice(max(0, sl.start), sl.stop)
                for dim, sl in sel.items()}

        # remove from indexer dims not in the DataArray object
        reduced_sel = {k: v for k, v in sel.items() if k in self.cfarray.dims}

        # select
        if len(reduced_sel) == 0:
            arr = self.cfarray
        else:
            arr = self._cfarray.isel(**reduced_sel, **isel_kwargs)

        # broadcast to extra dims if requested
        if broadcast_coords is not None:

            arr = self._broadcast_coords(
                arr,
                broadcast_coords=[
                    coord.isel({k: v for k, v in sel.items() if k in
                                coord.dims})
                    for coord in broadcast_coords])

        if as_science_dtype:
            arr = arr.fillna(self.fill_value).astype(
                self.science_dtype, copy=False)

        if padding:
            arr = self._pad_data(
                self.cfarray, arr,
                either_dict_or_kwargs(indexers, indx_kwargs, "isel"))

        # fix longitudes in [0, 360] range instead of [-180, 180]
        if arr.name == 'lon' and self.longitude180:
            if arr.max() >= 180.:
                if isinstance(arr, np.ndarray) and not arr.flags.writeable:
                    arr = arr.copy()
                arr[arr >= 180.] -= 360

        if as_masked_array:
            arr = arr.cb.to_masked_array()

        return arr

    @property
    def loc(self) -> _CLocIndexer:
        """Attribute for location based indexing like pandas."""
        return _CLocIndexer(self._cfarray)

    @property
    def mask(self) -> T.Union[np.ndarray, bool]:
        """Return the mask of the data (like in numpy MaskedArray)

        Masked values are NaN and values equal to the fill value
        """
        # mask NaN
        mask = np.ma.make_mask(
            ~np.isfinite(self.cfarray), shrink=True, copy=False)

        # mask where fill value
        if self.fill_value is not None:
            fv_mask = np.ma.make_mask(
                self.cfarray == self.fill_value, shrink=True,
                copy=False)

            mask = np.ma.mask_or(mask, fv_mask)

        return mask

    @classmethod
    def _replace_fill_value(cls, arr, previous, new):
        if previous not in arr:
            return arr

        encoding = arr.encoding.copy()
        attrs = arr.attrs.copy()
        # @TODO does a copy? should replace inline
        arr = arr.where(arr != previous, new)

        # restore attrs (mimic option keep_attrs in where method missing
        # in older versions of xarray)
        arr.encoding = encoding
        arr.attrs = attrs

        return arr

    def to_masked_array(self) -> np.ma.MaskedArray:
        """

        Returns:

        """
        arr = self.cfarray.to_masked_array(copy=False)

        if self.science_dtype != self.cfarray.dtype:
            # convert to original science dtype
            arr = arr.astype(self.science_dtype, copy=False)

        if self.fill_value is not None:
            if arr.fill_value is not None and arr.fill_value != self.fill_value:
                # xarray has defined its own fill value and cerbere has its
                # own - we can have only one fill value in the data
                arr = np.ma.masked_equal(
                    self._replace_fill_value(
                        arr, arr.fill_value, self.fill_value),
                    self.fill_value, copy=False)

            arr.set_fill_value(self.fill_value)

        return arr

    @classmethod
    def _pad_data(
            cls,
            array: xr.DataArray,
            subset: xr.DataArray,
            index: T.Optional[T.Mapping[str, slice]]
    ) -> xr.DataArray:
        """
        pad with fill values the ``subset`` array extracted from ``array``
        where ``index`` is beyond the limits of ``array``.
        """
        if len(array.shape) == 0:
            # dimensionless field
            return subset

        # determine required padding for each dim
        pad_edges = []
        for dim in list(array.dims):
            if dim in index:
                dslice = index[dim]
                pad_edges.append([
                    abs(min(0, dslice.start)),
                    abs(min(0, array.sizes[dim] - dslice.stop))
                ])
            else:
                pad_edges.append([0, 0])

        if all([_ == [0, 0] for _ in pad_edges]):
            # no padding necessary
            return subset

        # pad data
        sdtype = subset.cb.science_dtype
        if not np.issubdtype(subset.dtype, np.floating):
            # transform to float64 as xarray would do
            subset = subset.astype(np.float64, copy=False)

        padded_values = np.pad(
            subset.to_masked_array(copy=False), pad_edges, 'constant',
            constant_values=np.nan)
        dims = {dim: padded_values.shape[i] for i, dim in enumerate(array.dims)}

        # pad coordinates
        coords = {}
        for k_coord, v_coord in subset.coords.items():

            # @TODO check side effects first
            # if index is None or \
            #         len(set(index.keys()).intersection(set(v_coord.dims))) == 0:
            #     coords[k_coord] = v_coord
            #     continue

            c_pad_edges = tuple([
                tuple(pad_edges[i]) for i, dim in enumerate(array.dims)
                if dim in v_coord.dims
            ])
            c_fill_value = subset[k_coord].cb.fill_value
            if c_fill_value is None:
                # create a valid fill value if there was none so far
                c_fill_value = cf.default_fill_value(
                    subset[k_coord].cb.science_dtype)
                v_coord.cb.fill_value = c_fill_value

            padded_arr = np.ma.masked_values(np.pad(
                v_coord.to_masked_array(copy=False),
                pad_width=c_pad_edges,
                mode='constant',
                constant_values=c_fill_value), c_fill_value, copy=False)

            coords[k_coord] = xr.DataArray(
                padded_arr,
                dims=v_coord.dims,
                attrs=v_coord.attrs
            )
            coords[k_coord].encoding = v_coord.encoding

        padded_values = xr.DataArray(
            data=padded_values,
            dims=dims,
            coords=coords,
            attrs=subset.attrs)
        padded_values.encoding = subset.encoding
        padded_values.cb.science_dtype = sdtype

        return padded_values

    def bitmask_or(self, meanings):
        """helper function to test specific bits in a CF compliant mask

        Bit (or flag) fields are arrays of integers where each bit has a
        specific meaning, described in a ``flag_meaning`` field attribute.
        Providing a list of the meanings to be tested in ``meaning``, a boolean
        mask if built, using the `or` logical operator, with a True value
        everywhere at least one of the provided meanings is set.

        The field must defined as in CF convention, with ``flags_masks``
        and ``flag_meanings`` field attributes.

        Args:
            meanings(list or str): a list of the meanings that have to be set
                or a str if only one bit is tested. Available meanings are
                listed in the ``flag_meanings`` attribute of the field.

        Returns:
            A boolean array.
        """
        if ('flag_meanings' not in self.cfarray.attrs or
                'flag_masks' not in self.cfarray.attrs):
            raise ValueError(
                'This is not mask field. Either flag_meanings or flag_masks '
                'is missing.'
            )

        # transform mask attributes to list if it is not the case
        allmeanings = self.cfarray.attrs['flag_meanings']
        if isinstance(allmeanings, str):
            allmeanings = [_ for _ in allmeanings.split(' ') if _ != '']

        allmasks = self.cfarray.attrs['flag_masks']
        if isinstance(allmasks, str):
            allmasks = [_ for _ in allmasks.split(' ') if _ != '']

        criteria = meanings
        if isinstance(meanings, str):
            criteria = [meanings]

        # calculate sum (and) of all mask bits requested to be set
        masksum = 0
        for criterium in criteria:
            try:
                bit = allmeanings.index(criterium)
            except:
                raise ValueError('Unknown flag meaning {}'.format(criterium))
            masksum += allmasks[bit]

        # calculate mask
        return self.cfarray & int(masksum) != 0

    def clip(
            self,
            geometry: shapely.geometry.Polygon,
            masked: bool = False,
            continuity_threshold: int = 0,
            as_masked_array: bool = True,
            **kwargs) -> T.List[T.Union[xr.DataArray, np.ma.masked_array]]:
        """Return the data of a field within a geographical area.

        Extract the subset(s) of the Dataset including the whole area geometry,
        defined as a polygon of lon/lat coordinates.

        Any keywords from :meth:`get_values()` can be applied here too.

        Args:
            geometry (shapely.geometry.Polygon): boundaries of the clipped data,
                as a polygon of lon, lat coordinates.

            continuity_threshold (int): maximum number of non-contiguous
                measurements allowed beyond which two datasets are extracted
                instead of one. Avoids creating too many subsets when lat/lon
                are not continuous.

            masked (bool): mask the data out of the geometry boundary.
                May take additional processing time.

            as_masked_array (bool): return result as a numpy masked array if
                True (default), or xarray DataArray if set to False.

        Return:
            data subset fitting the clip area, as a xarray DataArray or numpy
            masked array, depending on ``as_masked_array`` value.
        """
        (lonmin, latmin, lonmax, latmax) = geometry.bounds

        # get spatial dimensions
        spatial_dims = list(self.cfarray.coords['lat'].dims)
        for d in self.cfarray.coords['lon'].dims:
            if d not in spatial_dims:
                spatial_dims.append(d)

        # coarse search on geometry bounding box - lat/lon need to be
        # broadcasted to the array spatial shape
        lat = self.cfarray.lat.cb.isel(
            broadcast_coords=[self.cfarray.coords[_] for _ in spatial_dims],
            as_masked_array=False)
        lon = self.cfarray.lon.cb.isel(
            broadcast_coords=[self.cfarray.coords[_] for _ in spatial_dims],
            as_masked_array=False)

        area_data = lat.where((
                (lon >= lonmin) & (lon <= lonmax) &
                (lat >= latmin) & (lat <= latmax)
        ))
        inside = ~area_data.to_masked_array().mask
        if continuity_threshold > 0:
            inside = binary_dilation(inside, iterations=continuity_threshold)
        slices = find_objects(label(inside)[0])

        # return all extracted subsets
        subsets = []
        for sl in slices:
            dslices = {d: sl[i] for i, d in enumerate(spatial_dims)}
            if 'index' in kwargs:
                if set(spatial_dims).intersection(kwargs['index'].keys()):
                    raise ValueError(
                        'slicing on spatial dimensions can not be used when '
                        'clipping data'
                    )
                dslices.update(kwargs.pop('index'))
            subsets.append(
                self.cfarray.cb.isel(dslices, **kwargs))

            if masked:
                # @TODO
                raise NotImplementedError

        return subsets
