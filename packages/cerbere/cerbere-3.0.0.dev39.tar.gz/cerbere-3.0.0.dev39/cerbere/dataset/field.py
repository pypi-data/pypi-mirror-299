# -*- coding: utf-8 -*-
"""
Classes for the handling the fields.
"""
from __future__ import absolute_import, division, print_function

import collections
import copy
import logging
from typing import Any, Hashable, List, Mapping, Optional, Tuple, Type, Union

try:
    # python >= 3.7.2
    from typing import OrderedDict
except ImportError:
    # python >= 3.6
    from typing import MutableMapping as OrderedDict

import warnings

import numpy as np
import xarray as xr

import cerbere.cfconvention as cf
import cerbere

__all__ = ['Field']


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


class Field(object):
    """A Field describes a scientific data array. It contains data and
    metadata attributes.

    This is an extension of xarray's DataArray with stricter requirements on
    attributes and the encoding of masked arrays.

    A :class:`Field` object can be attached to a  :class:`~cerbere.dataset.dataset.Dataset`
    object (of any class inherited from a :class:`~cerbere.dataset.dataset.Dataset`,
    provided with the ``dataset`` argument.

    Args:
        data: the scientific data. Can be of the following types:

              * :class:`np.ma.MaskedArray`
              * :class:`xarray.DataArray`

            Optional (the field can be created with default values)

        name: the label of the field (don't use any white space). This
            corresponds to the variable name in a netcdf file

        dims (tuple or OrderedDict): the scientific array dimension names. If no
            data are provided (new masked field), provide dimension names and
            sizes as a dictionary.

        dtype: the type of the data. Infer the type from the provided data by
            default. xarray changes the data type of arrays when using masking,
            defining the field true type with this keyword will ensure you
            always get the data in the expected dtype when accessing with
            `get_values` method. Data will also be saved with the expected
            dtype.

        precision (int, optional): number of significant digits (when writing
            the data on file)

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

        attrs (dict) : a dictionary of the metadata associated with the field's
            values.
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
    def __init__(self,
                 data,
                 name: Optional[Hashable] = None,
                 dims: Optional[
                     Union[Tuple[str, ...], OrderedDict[Hashable, int]]] = None,
                 dtype: Optional[Union[np.dtype, Type[float]]] = None,
                 components: Optional[Tuple['Field']] = None,
                 dataset: Optional['Dataset'] = None,
                 fill_value: Optional[Any] = None,
                 no_missing_value: bool = False,
                 precision: Optional[int] = None,
                 description: Optional[str] = None,
                 standard_name: Optional[Union[str, Tuple[str, str]]] = None,
                 units: Optional[str] = None,
                 quality_vars: Optional[List[str]] = None,
                 attrs: Optional[Mapping[str, Any]] = None,
                 encoding: Optional[Mapping[str, Any]] = None,
                 **kwargs) -> None:
        """
        """
        self._array = cerbere.new_array(
            data,
            name=name,
            dims=dims,
            science_dtype=dtype,
            fill_value=fill_value,
            precision=precision,
            long_name=description,
            standard_name=standard_name,
            units=units,
            ancillary_variables=quality_vars,
            attrs=attrs,
            **kwargs
        )
        if encoding is not None:
            self._array.cerbere.cfdataset.encoding.update(encoding)

        if no_missing_value:
            self._array.cerbere.fill_value = None

    @classmethod
    def to_field(cls, data: xr.DataArray) -> 'Field':
        """Cast a xarray DataArray to a
        :class:`cerbere.datamodel.field.Field` object
        """
        return Field(data=data)

    def to_xarray(
            self,
            silent: bool = False,
            decoding: bool = False) -> xr.DataArray:
        """
        Return the field values a xarray DataArray

        Args:
            decoding: return the DataArray in its scientific dtype instead of
                its DataArray dtype.
        """
        if decoding:
            return self._array.cerbere.cfarray.astype(
                self._array.cerbere.science_dtype)

        return self._array.cerbere.cfarray

    def __str__(self):
        return self._array.cerbere.__str__()

    @property
    def name(self) -> Hashable:
        """Name of the field"""
        return self._array.cerbere.cfarray.name

    @name.setter
    def name(self, value: Hashable):
        self._array.cerbere.cfarray.name = value

    @property
    def attrs(self) -> Mapping[Hashable, Any]:
        """A dict of the field attributes"""
        return self._array.cerbere.cfarray.attrs

    @attrs.setter
    def attrs(self, attrs: Mapping[Hashable, Any]):
        self._array.cerbere.cfarray.attrs = attrs

    @property
    def encoding(self) -> Mapping[Hashable, Any]:
        """A dict of the field encoding attributes"""
        return self._array.cerbere.cfarray.encoding

    @encoding.setter
    def encoding(self, attrs: Mapping[Hashable, Any]):
        self._array.cerbere.cfarray.encoding = attrs

    @property
    def sizes(self) -> Mapping[Hashable, int]:
        """A tuple of the field dimensions name and size"""
        if self.dataset is None:
            return self._array.cerbere.cfarray.sizes
        else:
            return self.dataset.get_field_sizes(self.name)

    @property
    def dims(self) -> Tuple[Hashable]:
        """A tuple of the field dimensions name and size"""
        return self._array.cerbere.cfarray.dims

    @dims.setter
    def dims(self, dims):
        self._array.cerbere.cfarray.dims = dims

    @property
    def dimnames(self) -> Tuple[Hashable]:
        """Tuple of the field's dimension names"""
        return self.dims

    def get_dimsize(self, dimname) -> int:
        """Return the size of a field dimension"""
        return self._array.cerbere.cfarray.sizes[dimname]

    @property
    def fill_value(self) -> Union[Any, None]:
        """The value for missing data in the field"""
        return self._array.cerbere.fill_value

    @fill_value.setter
    def fill_value(self, fill_value: Any):
        """set the value for missing data"""
        self._array.cerbere.fill_value = fill_value

    @property
    def precision(self) -> Union[int, None]:
        """The least significant digit for the values of the field.

        Used for storage optimization when writing on disk. The least
        significant digit is the power of ten of the smallest decimal place in
        the data that is a reliable value.
        """
        return self._array.cerbere.precision

    @precision.setter
    def precision(self, precision: int):
        """Set the least significant digit for the values of the field.

        Used for storage optimization when writing on disk. The least
        significant digit is the power of ten of the smallest decimal place in
        the data that is a reliable value.
        """
        self._array.cerbere.precision = precision

    @property
    def valid_min(self) -> Union[Any, None]:
        """The minimum valid value in the field data"""
        return self._array.cerbere.valid_min

    @valid_min.setter
    def valid_min(self, value: Any):
        """set the minimum valid value"""
        self._array.cerbere.valid_min = value

    @property
    def valid_max(self) -> Union[Any, None]:
        """The maximum valid value in the field data"""
        return self._array.cerbere.valid_max

    @valid_max.setter
    def valid_max(self, value: Any):
        """set the maximum valid value"""
        self._array.cerbere.valid_max = value

    @property
    def units(self) -> Union[str, None]:
        """The field data units (``units`` CF attribute)"""
        return self._array.cerbere.units

    @units.setter
    def units(self, units: str):
        """Set the field data units (``units`` CF attribute)"""
        self._array.cerbere.units = units

    @property
    def description(self) -> Union[str, None]:
        """The field description (``long_name`` CF attribute)"""
        return self._array.cerbere.long_name

    @description.setter
    def description(self, description: str) -> None:
        """set the field description (``long_name`` CF attribute)"""
        self._array.cerbere.long_name = description

    @property
    def standard_name(self) -> Union[str, None]:
        """The field standard name (``standard_name`` CF attribute)"""
        return self._array.cerbere.standard_name

    @standard_name.setter
    def standard_name(self, standard_name: str) -> None:
        """set the standard_name (``standard_name`` CF attribute)"""
        if isinstance(standard_name, tuple):
            self._array.cerbere.standard_name = standard_name[0]
            self._array.cerbere.authority = standard_name[1]
        elif standard_name is not None:
            self._array.cerbere.standard_name = standard_name
            self._array.cerbere.authority = cf.CF_AUTHORITY

    @property
    def components(self):
        """subfield of a multi-array field (such as vector, broken down into
        u and v fields)"""
        raise DeprecationWarning

    @name.setter
    def components(self, value):
        raise DeprecationWarning

    @property
    def dtype(self) -> np.dtype:
        """The type of the field data"""
        return self._array.cerbere.science_dtype

    def is_composite(self) -> bool:
        """
        True if the field is a composite field.

        A composite field is a composition of sub fields (vector components,
        real and imaginary part of a complex, ...)
        """
        raise DeprecationWarning

    def is_axis(self, axis: str) -> bool:
        """Returns true if the field is the coordinate field for the given axis.

        Args:
            axis: axis name (among X, Y, Z, T)
        """

    def get_values(
            self,
            index: Optional[Mapping[str, slice]] = None,
            padding: Optional[bool] = False,
            **kwargs) -> np.ma.MaskedArray:
        """
        Return the field values as a :class:`np.ma.MaskedArray` object.

        Args:
            index: any kind of xarray indexing compatible with xarray
                :func:`~xarray.DataArray.isel` selection method.

            padding: pad the result with fill values where slices are out of the
             field dimension limits. Default is False.

        Returns:
            The field values as a np MaskedArray

        """
        return self._array.cerbere.isel(
            index, padding=padding, as_masked_array=True, **kwargs)

    def get_xvalues(
            self,
            index: Optional[Mapping[str, slice]] = None,
            padding: Optional[bool] = False,
            **kwargs) -> xr.DataArray:
        """
        Return the field values as a :class:`xarray.DataArray` object.

        Args:
            index: any kind of xarray indexing compatible with
                :func:`xarray.DataArray.isel` selection method.

            padding: pad the result with fill values where slices are out of the
             field dimension limits. Default is False.

        Returns:
            The field values as a xarray DataArray

        """
        return self._array.cerbere.isel(
            index, padding=padding, as_masked_array=False, **kwargs)

    def set_values(
            self,
            values: Union[np.ndarray, np.ma.MaskedArray],
            index: Optional[Mapping[str, slice]] = None,
            **kwargs) -> None:
        """set the values of a field.

        It is  possible to set only a subset of the field data array, using
        ``index``:

        >>> import numpy as np
        >>> data = np.ma.zeros((100, 200))
        >>> field = Field(data, name='test', dims=('x', 'y'))
        >>> field.set_values(
        >>>        np.full((10, 5,), 2),
        >>>        {'x': slice(10, 20), 'y': slice(0, 5)}
        >>>        )

        Args:
            values: the values to replace the ones in the field
            index: a dict of slices or indices of the subset to replace in the
                current field data array

        """
        if index is None:
            self._array[:] = values
        else:
            self._array.loc[index] = values

    def is_saved(self):
        """
        Return True is the content of the field is saved on file and
        was not updated since
        """
        raise DeprecationWarning

    def bitmask_or(
            self,
            meanings,
            index: Mapping[Hashable, Any]=None,
            **kwargs):
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
        return self._array.cerbere.isel(index, **kwargs).cerbere.bitmask_or(
            meanings)

    @classmethod
    def compute(
            cls,
            func,
            field1: 'Field', field2: 'Field'=None,
            **kwargs) -> 'Field':
        """Apply a function to a field (possibly combining with a second one)
         and returns the result as a new field.

        The function may be for instance a np MaskedArray operator
        such as np.ma.anom, np.ma.corr,...

        To be used with caution.

        Args:
            func (function) : the function to be called (ex: np.ma.anom)
            field1 (Field) : the field argument to the function
            field2 (Field, optional) : an optional 2nd field argument to the
                function
            kwargs : any argument to Field creation further describing the
                returned Field (units, name, ...).

        Returns:
            Field: the result field
        """
        if 'name' not in kwargs:
            varname = 'result'
        if field2 is None:
            values = func(field1.get_values())
        else:
            values = func(field1.get_values(), field2.get_values())
        field = Field(data=values,
                      name=varname,
                      dims=copy.copy(field1.dims),
                      dtype=field1.dtype,
                      fill_value=field1.fill_value,
                      **kwargs)
        return field

    def clone(
            self,
            index: Mapping[Hashable, Any] = None,
            padding: bool = False,
            prefix: str = None,
            **kwargs) -> 'Field':
        """Create a copy of a field, or a subset defined by index, and
        padding out as required.

        The data are also copied.

        The returned field does not contain any attachment to the source file
        attached to the original field, if any.

        Args:
            index (dict, optional):any kind of xarray indexing compatible with
                xarray :func:`~xarray.DataArray.isel` selection method.
            padding (bool, optional): True to pad out feature with fill values
                to the extent of the dimensions.
            prefix (str, optional): add a prefix string to the field names of
                the extracted subset.
        """
        if index is None:
            new_field = Field(
                data=self._array.copy(deep=True)
            )
        else:
            new_index = {
                dim: val
                for dim, val in index.items() if dim in self._array.dims
            }
            subarray = self._array[new_index]
            if padding:
                data = self.__pad_data(subarray.values, new_index)
                subarray.set_values(data)

            new_field = Field(data=subarray.copy(deep=True))

        # # copy cerbere internal encoding attributes...
        # new_field.encoding['cerbere'] = copy.copy(
        #     self._array.encoding['cerbere'])
        #
        # # ...but detach from any parent dataset
        # self.detach()

        if prefix is not None:
            new_field.set_name(prefix + new_field.name)
        return new_field

    def detach(self):
        self.dataset = None

    def rename(self, newname: str) -> None:
        """Rename the field inplace.

        Args:
            newname (str): new name of the field
        """
        self.name = newname

    def __add__(self, other: 'Field') -> 'Field':
        """Return a new field with the sum of current and an other field."""
        res = Field.convert_from_xarray(self.xrdata + other.xrdata)
        res.xrdata.name = '{}_{}_sum'.format(self.name, other.name)
        return res

    def __sub__(self, other: 'Field') -> 'Field':
        """Return a new field with the difference of current and an other
        field.
        """
        res = Field.convert_from_xarray(self.xrdata - other.xrdata)
        res.xrdata.name = '{}_{}_difference'.format(self.name, other.name)
        return res

    def module(self) -> 'Field':
        """Return the module field from its eastward and northward components.

        The module is sqrt(u² + v²)

        Returns:
            Field: the module field
        """
        u, v = self.components
        values = np.ma.sqrt(
            np.ma.power(u.get_values(), 2) +
            np.ma.power(v.get_values(), 2)
        )
        if 'eastward_' in u.name:
            modname = u.name.replace('eastward_', '')
        else:
            modname = 'module'
        field = Field(
            values,
            name=modname,
            dims=u.dims,
            dtype=u.dtype,
            fill_value=u.fill_value,
            units=u.units
        )
        return field
