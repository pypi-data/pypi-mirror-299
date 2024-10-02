# -*- coding: utf-8 -*-
"""
Base class for any `cerbere` dataset. Built as a wrapper around a
:class:`~xarray.Dataset` object.
"""
import copy
import datetime
import glob
import logging
import os
import warnings
from abc import ABC
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Hashable, List, Mapping, MutableMapping, Optional, Tuple, Union
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import shapely.geometry
import xarray as xr
from dateutil import parser
from scipy.ndimage import find_objects, label, binary_dilation

import cerbere.cfconvention
import cerbere.dataset as internals
import cerbere.accessor.cdataset

from ..cfconvention import CF_AUTHORITY, DEFAULT_TIME_UNITS, default_profile
from .field import Field


# opening modes
class OpenMode(Enum):
    """
    ENUM to hold the allowed values for opening resources
    """
    READ_ONLY: str = 'r'
    WRITE_NEW: str = 'w'
    READ_WRITE: str = 'r+'

# attribute for override dtype
C_DTYPE = 'cerbere_dtype'

# standard geolocation coordinates
GEOCOORDINATES = [u'time', u'lat', u'lon', u'z', u'depth', u'height']
REQUIRED_GEOCOORDINATES = [u'time', u'lat', u'lon']

# standard attributes for geolocation coordinates
AXIS = {'lat': 'Y', 'lon': 'X', 'time': 'T',
        'z': 'Z', 'depth': 'Z', 'height': 'Z'}
STANDARD_NAME = {
    'lat': 'latitude',
    'lon': 'longitude',
    'time': 'time'
}
STANDARD_Z_FIELD = ['depth', 'height', 'alt', 'z']

# CDM feature types
CDM_TYPES = {
    'swath': 'Swath',
    'grid': 'Grid'
}

# common matching dimensions and fields in netCDF files
DIM_MATCHING = {
    'time': 'time',
    'lon': 'lon',
    'longitude': 'lon',
    'lat': 'lat',
    'latitude': 'lat',
    'x': 'x',
    'y': 'y',
    'mes': 'station',
    'station': 'station',
    'ni': 'cell',
    'cell': 'cell',
    'ra_size': 'cell',
    'col': 'cell',
    'nj': 'row',
    'row': 'row',
    'az_size': 'row',
    'depth': 'z',
    'height': 'z',
    'rows': 'row',
    'columns': 'cell',
    'NUMROWS': 'row',
    'NUMCELLS': 'cell',
    'across_track': 'cell',
    'along_track': 'row',
    'TIME': 'time',
    'LATITUDE': 'lat',
    'LONGITUDE': 'lon',
    'DEPTH': 'z'
}

FIELD_MATCHING = {
    'time': 'time',
    'longitude': 'lon',
    'latitude': 'lat',
    'lon': 'lon',
    'lat': 'lat',
    'depth': 'depth',
    'height': 'alt',
    'TIME': 'time',
    'LATITUDE': 'lat',
    'LONGITUDE': 'lon',
    'DEPTH': 'depth',
    'DEPH': 'depth',
}

TIME_COVERAGE_ATTRS = {
    'date': {
        'start': 'start_date',
        'end': 'stop_date'
    },
    'time': {
        'start': 'start_time',
        'end': 'stop_time'
    },
    'time_coverage': {
        'start': 'time_coverage_start',
        'end': 'time_coverage_end'
    },
    'time_coverage2': {
        'start': 'time_coverage_start',
        'end': 'time_coverage_stop'
    },
    'meas_time': {
        'start': 'first_meas_time',
        'end': 'lastst_meas_time'
    },
}

BBOX_CORNERS = {
    'latmin': [
        'southernmost_latitude', 'geospatial_lat_min', 'south_latitude'
    ],
    'latmax': [
        'northernmost_latitude', 'geospatial_lat_max', 'north_latitude'
    ],
    'lonmin': [
        'westernmost_longitude', 'geospatial_lon_min', 'west_longitude'
    ],
    'lonmax': [
        'easternmost_longitude', 'geospatial_lon_max', 'east_longitude'
    ]
}

class Dataset(ABC):
    """
    The `cerbere` dataset base class.

    A :class:`Dataset` object is internally built by composition over
    :class:`xarray.Dataset` objects.

    A :class:`Dataset` object can be created in different ways:
      * from a file (or list of files), giving its full path or URL
      * from a xarray :class:`xarray.Dataset` object
      * from a dict, using xarray syntax
      * from another :class:`Dataset` object

    Creating a Dataset from a file:

    >>> from cerbere.dataset.dataset import Dataset
    >>> dst = Dataset('./mydatafile.nc')

    Creating a Dataset from an xarray :class:`xarray.Dataset` object:
    The :mod:`xarray` object must have latitude, longitude and time coordinates
    with valid `cerbere` names (``lat``, ``lon``, ``time``):

    >>> import xarray as xr
    >>> import numpy as np
    >>> xrobj = xr.Dataset(
        coords={
            'lat': np.arange(0,10, 0.1),
            'lon': np.arange(5,15, 0.1),
            'time': np.full((100,), np.datetime64(('2010-02-03'), dtype='D'))
            },
        data_vars={'myvar': (('time',), np.ones(100))}
        )
    >>> dst = Dataset(xrobj)

    Creating a dataset from a dictionary:
    Using the same syntax as xarray (see:
    http://xarray.pydata.org/en/stable/generated/xarray.Dataset.from_dict.html#xarray.Dataset.from_dict).
    The provided dict must have latitude, longitude and time coordinates
    with valid `cerbere` names (``lat``, ``lon``, ``time``):

    >>> dst = Dataset(
            {'time': {'dims': ('time'), 'data': [datetime(2018, 1, 1)]},
             'lat': {'dims': ('lat'), 'data': np.arange(-80, 80, 1)},
             'lon': {'dims': ('lon',), 'data': np.arange(-180, 180, 1)},
             'myvar': {'dims': ('lat', 'lon',),
                       'data': np.ones(shape=(160, 360))}
             }
        )

    >>> dst = Dataset(
            {'coords': {
                'time': {'dims': ('time'), 'data': [datetime(2018, 1, 1)],
                         'attrs': {'units': 'seconds since 2001-01-01 00:00:00'}},
                'lat': {'dims': ('lat'), 'data': np.arange(-80, 80, 1)},
                'lon': {'dims': ('lon',), 'data': np.arange(-180, 180, 1)},
            },
            'attrs': {'gattr1': 'gattr_val'},
            'dims': ('time', 'lon', 'lat'),
            'data_vars': {'myvar': {'dims': ('lat', 'lon',),
                                    'data': np.ones(shape=(160, 360))}}}
        )

    :class:`Field` objects can also be mixed in:

    >>> field = Field(
            np.ones(shape=(160, 360)),
            'myvar',
            dims=('lat', 'lon',),
            attrs={'myattr': 'attr_val'}
        )
    >>> dst = Dataset(
            {'time': {'dims': ('time'), 'data': [datetime(2018, 1, 1)]},
             'lat': {'dims': ('lat'), 'data': np.arange(-80, 80, 1)},
             'lon': {'dims': ('lon',), 'data': np.arange(-180, 180, 1)},
             'myvar': field
             }
        )

    Args:

        dataset (str, list[str], xarray.Dataset): full path to a file from
            which to read the dataset content. It can be also a list of paths or
            a regular expression, if the mapper allows to open several files at
            once. Multiple files can only be opened in READ_ONLY mode.

        mode (enum, optional): access mode ('r', 'w', 'r+') when accessing a
            file.

        view (dict, optional): a dictionary where keys are dimension names
            and values are slices. A view can be set on a file, meaning
            that only the subset defined by this view will be accessible.
            This view is expressed as any subset (see :func:`get_values`).
            For example:

            >>> view = {'time':slice(0,0), 'lat':slice(200,300),
            >>>         'lon':slice(200,300)}

        dim_matching (dict): explicitly provides the matching between file
            native dimensions (keys) and their CF/cerbere standard name
            (values).

        field_matching (dict): explicitly provides the matching between file
            native fields (keys) and their CF/cerbere standard name (values).

        kwargs (dict): any argument to be passed on to the xarray
            open_dataset or open_mfdataset function.

    """
    def __init__(self,
                 dataset: Union[str, Path, xr.Dataset, 'Dataset', dict] = None,
                 mode: OpenMode = OpenMode.READ_ONLY,
                 dim_matching: Dict[str, str] = DIM_MATCHING,
                 field_matching: Dict[str, str] = FIELD_MATCHING,
                 attr_matching: Optional[Dict[str, str]] = None,
                 as_z: Optional[str] = None,
                 format: str = None,
                 attrs: Optional[Dict[str, str]] = None,
                 **kwargs):
        """
        """
        if 'view' in kwargs:
            raise DeprecationWarning('"view" keyword is deprecated and will '
                                     'not be taken into account')

        if dataset is None and 'data_vars' not in kwargs:
            raise ValueError('an url or dataset object must be provided')

        object.__init__(self)

        self.dataset = None

        # memorize opening arguments
        self._mode = OpenMode(mode)
        self._format = format
        self._url = None

        if isinstance(dataset, (str, list, Path)):
            if mode in ['w', 'rw']:
                self.dataset = xr.open_dataset(
                    dataset, mode=mode, format=format, **kwargs)
                return

            self.dataset = cerbere.open_dataset(dataset, **kwargs)

        elif isinstance(dataset, xr.Dataset):
            self.dataset = dataset

        elif isinstance(dataset, dict) or dataset is None:
            # dataset provided as a xarray compliant dictionary or xarray
            # dataset creation keywords
            if dataset is not None and 'data_vars' in kwargs:
                raise ValueError(
                    'data fields can not be provided both as main argument'
                    ' and with data_vars keyword'
                )
            if dataset is None and 'data_vars' not in kwargs:
                raise ValueError(
                    'either dataset or data_vars argument must be provided'
                )

            def data_as_tuple(arg):
                if not isinstance(arg, dict) or len(arg) == 0:
                    raise TypeError('Badly formatted input: {}'.format(arg))
                return isinstance(arg[next(iter(arg))], tuple)

            if dataset is None or data_as_tuple(dataset):
                # xarray from classic arguments
                dst = {'data_vars': dataset}
                for kw in ['data_vars', 'coords', 'attrs', 'dims']:
                    if kw in kwargs:
                        dst[kw] = kwargs[kw]
                self.dataset = xr.Dataset(**dst)
            else:
                # xarray from_dict
                self._create_from_dict(dataset)
        elif isinstance(dataset, Dataset):
            self.dataset = dataset.dataset
        else:
            raise TypeError(
                'Incorrect type {} to create a cerbere dataset object'
            )

        # add global attributes
        if attrs is not None:
            for attr, val in attrs.items():
                self.attrs[attr] = val

        if not isinstance(dataset, Dataset):
            if self.is_empty():
                return

        # standardize dataset
        self.dataset.cb.cerberize()
        # @TODO: not clear why the line above is not sufficient
        self.dataset = self.dataset.cb.cfdataset

        # set Z coordinate
        if as_z is not None:
            self.set_as_z(as_z)

    def set_as_z(self, fieldname: str, positive=None):
        """Set a field as representing the Z coordinate"""
        self.dataset.cb.set_as_z(fieldname, positive=positive)

    def to_xarray(self):
        """returns the Dataset as a xarray dataset object.

        Normally returns the underlying storage xarray dataset used in the
        Cerbere Dataset object if fitting the specifications of Cerbere well
        formed Dataset or Feature classes. If not, some transformation is
        performed to return a well formed xarray Dataset, which may take some
        computational time.
        """
        return self.dataset.cb.cfdataset

    @property
    def _dataset_class(self):
        return self.__class__.__name__

    def __str__(self):
        return self._std_dataset.cerbere.__str__()

    def _create_from_dict(self, data, **kwargs):
        """
        Create the dataset from a dict of fields and attributes.
        """
        # addition to xarray : fields can be provided as Field object
        def to_dict(arr):
            return {'dims': arr.dims, 'data': arr.data, 'attrs': arr.attrs}

        for var in data.keys():
            if isinstance(data[var], Field):
                data[var] = to_dict(data[var].to_xarray())

        if 'coords' in data.keys():
            for var, value in data['coords'].items():
                if isinstance(value, Field):
                    data[var] = to_dict(value.to_xarray())
        if 'data_vars' in data.keys():
            for var, value in data['data_vars'].items():
                if isinstance(value, Field):
                    data[var] = to_dict(value.to_xarray())

        # create a dataset
        self.dataset = xr.Dataset.from_dict(data)

        # assign coordinates
        for coord in REQUIRED_GEOCOORDINATES:
            if coord in self.dataset.data_vars:
                self.dataset = self.dataset.assign_coords(
                    {coord: self.dataset.data_vars[coord]}
                )

    def _check_mandatory_geocoordinates(self) -> bool:
        """check the required geolocation coordinates are in the dataset"""
        coord_validity = all([
            coord in self.coordnames
            for coord in REQUIRED_GEOCOORDINATES
        ])

        if not coord_validity:
            for coord in REQUIRED_GEOCOORDINATES:
                if coord not in self.coordnames:
                    logging.warning(
                        '  => Missing coordinate var: {}'.format(coord)
                    )
        return coord_validity

    def is_empty(self) -> bool:
        """Returns True if the dataset object contains no data yet"""
        return self.dataset.cb.cfdataset.equals(xr.Dataset())

    def __is_remote(self):
        """check is the url corresponds to a remote file (http, ftp,...)"""
        try:
            result = urlparse(self._url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @classmethod
    def exists(cls, url: Union[str, Path]) -> bool:
        """Returns True if `url` is an existing resource"""
        if isinstance(url, Path):
            return url.exists()
        try:
            result = urlparse(url)
            if len(result.scheme) == 0:
                return os.path.exists(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @classmethod
    def _get_time_format(cls):
        return '%Y-%m-%dT%H:%M:%SZ'

    def has_field(self, fieldname: str) -> bool:
        """Return True if the field ``fieldname`` exists in the dataset."""
        return fieldname in self.fieldnames

    def rename_field(self, name: str, newname: str) -> None:
        """Rename a field.

        Args:
            name (str): name of the field to be renamed
            newname (str): new name of the field
        """
        self.dataset.cb.cfdataset = self.dataset.cb.cfdataset.rename(
            {name: newname})

    @property
    def url(self) -> Path:
        """Return the url of the file storing the dataset"""
        return self.dataset.cb.url

    @property
    def basename(self) -> str:
        """Return the basename of the file storing the dataset"""
        return os.path.basename(self.url)

    @property
    def _std_dataset(self) -> xr.Dataset:
        """The standardized xarray dataset object containing the data.

        Use with caution as dynamic transformations may not be applied (for
        better performances or memory occupation). You may retrieve a feature
        object that is no more generic. It is safer to use the
        :meth:`~cerbere.dataset.dataset.as_dataset` method (future release).
        """
        return self.dataset.cb.cfdataset

    @_std_dataset.setter
    def _std_dataset(self, value: Union['xr.Dataset', 'Dataset']) -> None:
        """The standardized version of the underlying xarray dataset object.

        Use with caution as dynamic transformations may not be applied (for
        better performances or memory occupation). You may retrieve a feature
        object that is no more generic. It is safer to use the
        :meth:`~cerbere.dataset.dataset.as_dataset` method (future release).
        """
        if not isinstance(value, (xr.Dataset, Dataset)):
            raise TypeError('Unknow type {} for _std_dataset'.format(
                type(value))
            )
        if isinstance(self.dataset, Dataset):
            self.dataset._std_dataset = value
        else:
            self.dataset = value

    def is_new(self) -> bool:
        """True if the storage is opened in (over)write mode"""
        return self._mode == OpenMode.WRITE_NEW

    def is_readonly(self) -> bool:
        """True if the file or resource is opened in read only mode"""
        return self._mode == OpenMode.READ_ONLY

    @property
    def filesize(self) -> int:
        """The dataset file size, in octets"""
        return self.dataset.cb.filesize()

    @property
    def file_creation_date(self) -> datetime.datetime:
        """The date the dataset file was generated"""
        return self.dataset.cb.file_creation_date()

    def has_coord(self, coord: Hashable) -> bool:
        """Return True if the coordinate field is defined"""
        return self.dataset.cb.has_coord(coord)

    @property
    def sizes(self) -> Mapping[Hashable, int]:
        """Mapping from dimension names to lengths."""
        return self.dims

    @property
    def dims(self) -> Mapping[Hashable, int]:
        """Mapping from dimension names to lengths.

        CF convention names are used whenever possible for the dimensions.
        """
        return OrderedDict(self._std_dataset.dims)

    @property
    def dimnames(self) -> Tuple[Hashable]:
        """Tuple of the dataset's dimension names"""
        return tuple(self.dims.keys())

    @property
    def dimsizes(self) -> Tuple[int]:
        """Tuple of the dataset's dimension sizes"""
        return tuple(self.dims.values())

    @property
    def attrs(self) -> MutableMapping[Hashable, Any]:
        """Mapping from global attribute names to value."""
        return self.dataset.attrs

    @attrs.setter
    def attrs(self, attrs):
        self.dataset.attrs = attrs

    def get_attr(self, attr: str) -> Any:
        """Returns the value of a global attribute.

        Args:
            attr(str): name of the global attribute.

        Returns:
            value of the requested attribute.
        """
        return self.dataset.attrs[attr]

    def get_dimsize(self, dimname: str) -> int:
        """Return the size of a dimension.

        Args:
            dimname (str): name of the dimension.

        Returns:
            int: size of the dimension.
        """
        return self.dims[dimname]

    def get_field_sizes(self, fieldname: Hashable) -> Mapping[Hashable, int]:
        """Mapping from dimension names to lengths of a field in the dataset

        Args:
            fieldname (str): name of the field
        """
        return OrderedDict(self._std_dataset[fieldname].sizes)

    def get_field_dims(self, fieldname: Hashable) -> Tuple[Hashable]:
        """Tuple of the dimension names of a field in the dataset

        Args:
            fieldname (str): name of the field
        """
        return tuple(self.get_field_sizes(fieldname).keys())

    @property
    def _varnames(self) -> List[Hashable]:
        """List of the names of all the fields (including coordinates) of the
        dataset.
        """
        return list(self._std_dataset.variables.keys())

    @property
    def coordnames(self) -> List[Hashable]:
        """List of names of the coordinate fields of the dataset."""
        return list(self._std_dataset.coords.keys())

    @property
    def geocoordnames(self) -> List[Hashable]:
        """List of names of the geospatial coordinate fields of the dataset."""
        return [
            k for k, v in self._std_dataset.coords.items() if 'axis' in v.attrs
        ]

    @property
    def coords(self) -> List['Field']:
        """List of coordinates (as Field objects)"""
        return [
            Field(v, name=k)
            for k, v in self._std_dataset.coords.items()
        ]

    @property
    def geocoords(self) -> List['Field']:
        """List of geolocation coordinates (as Field objects)"""
        return [
            Field(v, name=k)
            for k, v in self._std_dataset.coords.items()
            if 'axis' in v.attrs
        ]

    @property
    def fieldnames(self) -> List[Hashable]:
        """The names of the geophysical fields of the mapper.

        The coordinate field names are excluded from this list.

        Returns:
            list[str]: list of field names
        """
        return list(self._std_dataset.data_vars.keys())

    def get_field(self, fieldname: str) -> 'Field':
        """
        Return the :class:`~cerbere.dataset.field.Field` object corresponding to
        the requested field name.

        The :class:`~cerbere.dataset.field.Field` class contains all the metadata
        describing a field (equivalent to a variable in netCDF).

        Args:
            fieldname (str): name of the field

        Returns:
            the corresponding Field object
        """
        if fieldname not in self.fieldnames:
            raise ValueError('Unknown field {}'.format(fieldname))

        return Field(self._std_dataset[fieldname], fieldname, dataset=self)

    def add_field(self, field: 'Field', force_index: bool = True) -> None:
        """Add a field to the feature.

        Args:
            field: the field is provided as a
                :class:`~cerbere.dataset.field.Field` object
            force_index: if the added field contains an index coordinate with
                the same name as the dataset, replace the values with those of
                the dataset (otherwise only the field values for which the index
                values of the field and the dataset are the same will be added).
        """
        if field.name in self.fieldnames:
            raise Exception(
                'Field already existing in feature. Can not add {}'
                .format(field.name)
            )

        try:
            dataarr = field.to_xarray(silent=True, decoding=False)

            # if some indexes are existing in the dataset, ensure the values are
            # the same
            for idx in dataarr.indexes:
                if idx in self._std_dataset.indexes and force_index:
                    dataarr = dataarr.reset_index(idx, drop=True)

            self._std_dataset = self._std_dataset.assign(
                {field.name: dataarr}
            )
        except ValueError:
            # an error case when for instance an index (like time) has masked
            # values. This seems to do the trick, in some tested cases but
            # probably not all of them...
            warnings.warn(
                'Entering a special case where not xarray variable '
                'assignment was possible, probably because of fill or duplicate'
                ' values in a coordinate. Field: {}'.format(field.name))
            self._std_dataset[field.name] = xr.DataArray(
                coords=[(d, self._std_dataset.coords[d].data)
                        for d in field.dims],
                data=field.get_values(),
                attrs=field.attrs)
            self._std_dataset[field.name].encoding = field.encoding
        except:
            raise

    def drop_field(self, fieldname: str):
        """Remove a field from the feature"""
        self._std_dataset = self._std_dataset.drop(fieldname)

    def get_coord(self, coordname: str) -> 'Field':
        """Returns the coordinate field with the requested name.
        """
        if coordname not in self.coordnames:
            raise ValueError(
                'Coordinate field {} is not exising: '.format(coordname)
            )

        return Field(
            self._std_dataset.coords[coordname], name=coordname, dataset=self
        )

    def get_geocoord(self, coordname: str) -> 'Field':
        """Returns the geolocation coordinate field with the requested name.

        Possible coordinate field names are 'lat', 'lon', 'time', 'z'.
        """
        if coordname not in ['lat', 'lon', 'time', 'z']:
            logging.warning(
                '{} is not a geolocation coordinate'.format(coordname)
            )
        return self.get_coord(coordname)

    def get_geocoord_by_axis(self, axis: str) -> 'Field':
        """Returns the geolocation coordinate field for the given axis.

        Possible coordinate field names are 'lat', 'lon', 'time', 'z'.
        """
        if axis not in ['X', 'Y', 'T', 'Z']:
            logging.warning(
                '{} is not a geolocation coordinate'.format(axis)
            )
        for coordname in self.geocoordnames:
            if self.get_coord(coordname).attrs['axis'] == axis:
                return self.get_coord(coordname)

        raise ValueError('No coordinate found for axis: {}'.format(axis))

    @property
    def geodims(self) -> MutableMapping[str, int]:
        """Mapping from geolocation dimension names to lengths.
        """
        return OrderedDict([
            (DIM_MATCHING[_], self.sizes[_]) for _ in list(self.dimnames)
            if _ in DIM_MATCHING.keys()
            ])

    @property
    def geodimnames(self) -> Tuple[str]:
        """A tuple of the dataset geolocation dimension names"""
        return tuple(self.geodims.keys())

    @property
    def geodimsizes(self) -> Tuple[int]:
        """A tuple of the dataset geolocation dimension sizes"""
        return tuple(self.geodims.values())

    def get_field_fillvalue(self, fieldname: str) -> Any:
        """Returns the missing value of a field"""
        if fieldname in self.coordnames:
            return self.get_coord(fieldname).fill_value
        else:
            return self.get_field(fieldname).fill_value

    def get_values(self,
                   fieldname: str,
                   index: Mapping[str, slice] = None,
                   as_masked_array: bool = True,
                   expand: bool = False,
                   expand_dims: List[str] = None,
                   **kwargs):
        """Read the data of a field.

        Args:
            fieldname (str): name of the field which to read the data from

            index: any kind of xarray indexing compatible with
                :func:`xarray.DataArray.isel` selection method.

            padding: pad the result with fill values where slices are out of the
             field dimension limits. Default is False.

            as_masked_array (bool, optional): return the result as a masked
                array instead of a xarray DataArray. Default is True (may had some
                overhead).

        Return:
            MaskedArray: array of data read. Array type is the same as the
                storage type.
        """
        if expand_dims is not None:
            expand_dims = [self._std_dataset[_] for _ in expand_dims]

        return self._std_dataset[fieldname].cerbere.isel(
            index, as_masked_array=as_masked_array,
            broadcast_coords=expand_dims, **kwargs
        )

    def set_mask(self, fieldname: str, mask: np.ndarray):
        raise DeprecationWarning()

    def set_values(
            self,
            fieldname: str,
            values: Union[np.ndarray, np.ma.MaskedArray],
            index: Optional[Mapping[str, slice]] = None,
            **kwargs):
        """set the values of a field.

        It is  possible to set only a subset of the field data array, using
        ``index``:

        >>> import numpy as np
        >>> ...
        >>> dst.set_values(
        >>>        'test',
        >>>        np.full((10, 5,), 2),
        >>>        {'x': slice(10, 20), 'y': slice(0, 5)}
        >>>        )

        See:
        Field.set_values

        """
        self._std_dataset[fieldname].cerbere.loc[index] = values

    def clip_values(
            self,
            fieldname: Hashable,
            geometry: 'shapely.geometry.Polygon',
            masked: bool = False,
            continuity_threshold: int = 0,
            as_masked_array: bool = True,
            **kwargs) -> List[Union['xr.DataArray', 'np.ma.masked_array']]:
        """Return the data of a field within a geographical area.

        Extract the subset(s) of the Dataset including the whole area geometry,
        defined as a polygon of lon/lat coordinates.

        Any keywords from :meth:`get_values()` can be applied here too.

        Args:
            fieldname (str): name of the field which to read the data from

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
        spatial_dims = list(self.get_field_dims('lat'))
        for d in self.get_field_dims('lon'):
            if d not in spatial_dims:
                spatial_dims.append(d)

        # coarse search on geometry bounding box
        lat = self.get_values(
            'lat', expand=True, expand_dims=spatial_dims, as_masked_array=False,
            **kwargs
        )
        lon = self.get_values(
            'lon', expand=True, expand_dims=spatial_dims, as_masked_array=False,
            **kwargs
        )
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
                self.get_values(fieldname, index=dslices, **kwargs)
            )

            if masked:
                raise NotImplementedError

        return subsets

    def get_times(self, as_masked_array=True, **kwargs):
        """Return the times of a feature.

        The time values are returned as numbers. Use the
        :func:`get_time_units` function to convert these values to date or
        time objects.

        Subsets can be returned by using either slices or indices arguments.
        slices and indices are exclusive and can not be both specified. Both
        must be provided as dictionaries where keys are the names of the
        dimensions to subset. Values are slice objects in the case of `slice`
        argument and numbers in the case of `indices` argument. Only the
        subsetted dimensions need to be provided (the full range s assumed for
        the other dimensions).

        Args:
            index: any kind of xarray indexing
            as_masked_array (bool): return the result as a numpy masked array
                (by default), or as a numpy ndarray if set to False.
            padding (bool) : if True, pad the result with fill values where
                slices are out of the field size.

        Returns:
            numpy.ma.array: the requested data.
        """
        return self.dataset['time'].cerbere.isel(
            as_masked_array=True, **kwargs)

    def get_time_units(self):
        """Return the time units as a CF convention compliant string"""
        warnings.warn(
            'Deprecated get_time_units function.',
            FutureWarning
        )
        return DEFAULT_TIME_UNITS

    def get_datetimes(self, slices=None, indices=None, **kwargs):
        """Return the time values of a feature as datetime objects.

        Subsets can be returned by using either slices or indices arguments.
        slices and indices are exclusive and can not be both specified. Both
        must be provided as dictionaries where keys are the names of the
        dimensions to subset. Values are slice objects in the case of `slice`
        argument and numbers in the case of `indices` argument. Only the
        subsetted dimensions need to be provided (the full range s assumed for
        the other dimensions).

        Args:
            slices (dictionary): a dictionary where keys are the dimensions
                to slice and values are slice objects.

            indices (list): a dictionary where keys are the dimensions
                to slice and values are slice objects.

            cache (bool): if cache is True, the data read from file are kept in
                memory. The full field data array is kept in cache, slices or
                indices are ignored by caching (though the result returned by
                this function will be a subset if slices or indices are
                provided. Use the `view` concept in mappers instead if you want
                frequent accesses to a subset of a file.
                Default is False.

        Returns:
            numpy.ma.array<datetime>: the requested data.

        Warning:
            To be used with caution as conversion to datetime objects can take
            a long time. Use only when accessing single elements for instance.
        """

        if 'as_masked_array' not in kwargs or kwargs['as_masked_array']:
            return (self.get_values('time', **kwargs)
                    .astype('datetime64[us]')
                    .astype(datetime.datetime))
        else:
            raise NotImplementedError

    def get_lon(self, **kwargs):
        """Return the longitude values of a feature.

        Subsets can be returned by using either slices or indices arguments.
        slices and indices are exclusive and can not be both specified. Both
        must be provided as dictionaries where keys are the names of the
        dimensions to subset. Values are slice objects in the case of `slice`
        argument and numbers in the case of `indices` argument. Only the
        subsetted dimensions need to be provided (the full range s assumed for
        the other dimensions).

        Args:
            index: any kind of xarray indexing
            as_masked_array (bool): return the result as a numpy masked array
                (by default), or as a numpy ndarray if set to False.
            padding (bool) : if True, pad the result with fill values where
                slices are out of the field size.

        Returns:
            numpy.ma.array<float>: the requested longitudes.
        """
        return self.get_values('lon', **kwargs)

    def get_lat(self, **kwargs):
        """Return the latitude values of a feature.

        Subsets can be returned by using either slices or indices arguments.
        slices and indices are exclusive and can not be both specified. Both
        must be provided as dictionaries where keys are the names of the
        dimensions to subset. Values are slice objects in the case of `slice`
        argument and numbers in the case of `indices` argument. Only the
        subsetted dimensions need to be provided (the full range s assumed for
        the other dimensions).

        Args:
            index: any kind of xarray indexing
            as_masked_array (bool): return the result as a numpy masked array
                (by default), or as a numpy ndarray if set to False.
            padding (bool) : if True, pad the result with fill values where
                slices are out of the field size.

        Returns:
            numpy.ma.array<float>: the requested latitudes.
        """
        return self.get_values('lat', **kwargs)

    def set_z(self, values, ztype='depth'):
        """Set the depth(s)

        Args:
            values (:class:`numpy.ma.MaskedArray` or :class:`Field`): depth
                values, as a array of floats or a Field object

            ztype (string): type is depth (positive down) or height (positive
                up)
        """
        coord = self._make_coord(
            'z', values, 'm', ztype, ztype
        )
        coord.attrs.update(
            {'depth': {'positive': 'down'},
             'height': {'positive': 'up'}
             }[ztype]
        )
        return coord

    def get_z(self, **kwargs):
        """
        if cache is True, data read from storage are kept in memory
        """
        return self.get_values('z', **kwargs)

    def extract(
            self,
            index: Optional[Mapping[str, slice]] = None,
            fields: Optional[List[str]] = None,
            padding: bool = False,
            prefix: Optional[str] = None,
            deep: bool = True,
            **kwargs
    ) -> 'Dataset':
        """
        Extract a subset of the dataset.

        If ``deep`` is False, returns only a view on the dataset, sharing the
        same data arrays in memory as the subsetted dataset.

        Args:
            index: any kind of xarray indexing compatible with
                :func:`xarray.DataArray.isel` selection method.

            padding: pad the result with fill values where slices are out of the
             field dimension limits. Default is False. ``deep`` must be set to
             True.

            fields: list of field names to extract. If None, all fields
                are extracted.

            prefix: add a prefix string to the field names of the returned
                subset.
        """
        if fields is not None and len(fields) > 0:
            dst = self._std_dataset[fields].cerbere.isel(
                index, padding=padding, prefix=prefix, **kwargs)
        else:
            dst = self._std_dataset.cerbere.isel(
                index, padding=padding, prefix=prefix, **kwargs)

        if deep:
            dst = dst.copy(deep=True)

        return Dataset(dst)

    def clip(
            self,
            geometry: shapely.geometry.Polygon,
            masked: bool = False,
            continuity_threshold: int = 0,
            **kwargs) -> List['Dataset']:
        """Return the dataset subsets within a geographical area.

        Extract the subset(s) of the Dataset including the whole area geometry,
        defined as a polygon of lon/lat coordinates.

        Any keywords from :meth:`extract()` can be applied here too.

        Args:
            geometry (shapely.geometry.Polygon): boundaries of the clipped data,
                as a polygon of lon, lat coordinates.

            continuity_threshold (int): maximum number of non-contiguous
                measurements allowed beyond which two datasets are extracted
                instead of one. Avoids creating too many subsets when lat/lon
                are not continuous.

            masked (bool, optional): mask the data out of the geometry boundary.
                May take additional processing time.

        Return:
            MaskedArray: array of data read. Array type is the same as the
                storage type.
        """
        return [Dataset(_) for _ in self._std_dataset.cerbere.clip(
                    geometry=geometry, masked=masked,
                    continuity_threshold=continuity_threshold, **kwargs)]

    def get_location_by_value(self, field, value, **kwargs):
        """Return the indices and geolocation of a given value.

        If the value is not unique, the first one found is returned.
        """
        if not np.isscalar(value):
            raise ValueError('value must be a scalar')

        loc = np.where(self.get_values(field, **kwargs) == value)
        loc = {dim: loc[i][0]
               for i, dim in enumerate(self.get_field(field).dimnames)}

        geoloc = (np.asscalar(self.get_lon(index=loc)),
                  np.asscalar(self.get_lat(index=loc)))

        return loc, geoloc,

    def closest_spatial_location(self, lon, lat):
        """Get closest dataset lat/lon location to given coordinates.

        Use pythagorian differences on lat/lon values so take the result with
        caution.

        Returns:
            A tuple with the indices and lon/lat of the closest point found.
        """
        d_lat = self.get_lat() - lat
        d_lon = self.get_lon() - lon

        if len(d_lat.shape) == 2:
            r2 = d_lat ** 2 + d_lon ** 2
            loc = np.where(r2 == np.min(r2))
            loc = {dim: loc[i][0]
                   for i, dim in enumerate(self.get_field_dims('lat'))}
            geoloc = (np.asscalar(self.get_lon(index=loc)),
                      np.asscalar(self.get_lat(index=loc)))
            return loc, geoloc,

        else:
            # @TODO
            raise NotImplementedError

    def clone(
            self,
            fieldname: str,
            **kwargs
    ):
        """
        Create a copy of a field, limiting to a set of slices or indices, and
        padding out as required.

        See:
            :func:`cerbere.dataset.field.Field.clone`
        """
        return self.dataset[fieldname].isel(**kwargs).copy(deep=True)

    def get_field_attrs(self, fieldname) -> Mapping[Hashable, Any]:
        """Returns the attributes of a field.

        Args:
            fieldname (str): name of the field.

        Returns:
            a dictionary where keys are the attribute names.
        """
        if isinstance(self.dataset, Dataset):
            return self.dataset.get_field_attrs(fieldname)

        return self.dataset[fieldname].attrs

    @property
    def time_coverage_start(self) -> datetime.datetime:
        """Minimum sensing time of the data contained in the dataset"""
        return self._std_dataset.cerbere.time_coverage_start

    @time_coverage_start.setter
    def time_coverage_start(self, date: datetime.datetime):
        """Set the minimum sensing time of the data contained in the dataset
        """
        self._std_dataset.cerbere.time_coverage_start = date

    @property
    def time_coverage_end(self) -> datetime.datetime:
        """Maximum sensing time of the data contained in the dataset"""
        return self._std_dataset.cerbere.time_coverage_end

    @time_coverage_end.setter
    def time_coverage_end(self, date: datetime.datetime):
        """Set the maximum sensing time of the data contained in the dataset
        """
        self._std_dataset.cerbere.time_coverage_start = date

    @property
    def bbox(self) -> 'shapely.geometry.Polygon':
        """The bounding box, e.g. the south/north and east/west
        limits of the feature.
        """
        return self._std_dataset.cerbere.bbox

    @bbox.setter
    def bbox(self,
             bbox: Union[str, tuple, 'shapely.geometry.Polygon'] = 'auto'):
        """Set the bounding box of the feature

        Args:
            :class:`shapely.geometry.Polygon`: the bounding box. If None, it is
                estimated from the feature lat/lon.
        """
        self._std_dataset.cerbere.bbox = bbox

    @property
    def wkt_bbox(self) -> str:
        """The bounding box in WKT format."""
        return self._std_dataset.cerbere.bbox.wkt

    def _get_attr_value(self, att: str) -> Any:
        """Return global attribute value or None if the attribute does not
        exists.
        """
        return self._std_dataset.attrs.get(att)

    def get_product_version(self):
        """return the product version"""
        return self._std_dataset.cerbere.product_version

    def close(self):
        """Close file"""
        pass

    @staticmethod
    def _xr_fillvalue(xvar, default=None):
        """Return the fill value of an xarray

        Which can be either in attrs or encoding attributes
        """
        return xvar.encoding.get(
            '_FillValue', xvar.attrs.get('_FillValue', default))

    @staticmethod
    def _xr_units(xvar, default=None):
        """Return the units of an xarray

        Which can be either in attrs or encoding attributes
        """
        return xvar.encoding.get('units', xvar.attrs.get('units', default))

    def save(self,
             dest: Union[str, 'Dataset', None] = None,
             format: str = 'NETCDF4',
             profile: str = 'default_saving_profile.yaml',
             force_profile: bool = False,
             keep_src_encoding: bool = False):
        """
        Args:
            dest (str, optional): save to a new file, whose path is provided in
                this argument. Raise an exception if the file already exists.
            profile (str, optional): path to a specific format profile to
                apply before saving (or default formatting profile is used).
            force_profile (bool, optional): force profile attribute values to
                supersede existing ones in dataset attributes.
            keep_src_encoding (bool): keep original dtype, _FillValue
                and scaling if any (through `add_offset` or `scale_factor`
                attributes) as in the source data.
        """
        if not isinstance(dest, (str, Path)):
            raise DeprecationWarning

        return self.dataset.cb.save(
                path=dest,
                format=format,
                profile=profile,
                force_profile=force_profile
            )

        # save as a new file
        if dest is not None:
            if isinstance(dest, (str, Path)):
                # save in a file
                if os.path.exists(str(dest)):
                    raise IOError('This file already exists')

                self._url = str(dest)
                self._mode = OpenMode.WRITE_NEW
                self._format = format
            elif isinstance(dest, Dataset):
                # if not dest.is_empty():
                #     raise IOError(
                #         'Can not save into a dataset that is not empty.'
                #     )
                if dest.is_readonly():
                    raise IOError('destination dataset is read-only')
                # use dest dataset as formatter
                dest.dataset = self.dataset.copy()
                return dest.save(
                    format=format,
                    profile=profile,
                    force_profile=force_profile
                )

        # save in the file currently attached to the dataset
        else:
            if self._mode == OpenMode.READ_ONLY:
                raise IOError(
                    'Can not save a dataset open in read only mode or with no '
                    'url provided'
                )

        # apply new formatting rules
        saved_dataset = self._convert_format(
            profile=profile, force_profile=force_profile)

        # remove internal special attributes
        for v in saved_dataset.variables.values():
            for att in ['_attached_dataset', '_components']:
                if att in v.attrs:
                    v.attrs.pop(att)

        # save to chosen format
        if 'NETCDF' in self._format:
            self._to_netcdf(saved_dataset, keep_src_encoding)

        else:
            logging.error('Unknown output format : {}'.format(self._format))
            raise NotImplementedError

    def add_global_attrs(
            cls,
            dataset: 'xr.Dataset',
            attrs: Mapping[str, Any],
            force_profile: bool = False) -> None:
        """Add default attributes to the dataset from a attribute definition
        file.

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

    def add_field_attrs(
            cls,
            dataset: xr.Dataset,
            attrs: Mapping[str, Any],
            force_profile: bool = False) -> None:
        """Add field attributes to the dataset from a attribute definition
        file.

        Args:
            attrs (dict): the field attributes to add when saving the dataset
        """
        # add attributes
        # don't override previous attribute values
        for v in attrs:
            if v not in dataset.variables:
                logging.warning(
                    'Field {} not found in the dataset to save. Skipping'
                    .format(v)
                )
                continue
            for att in attrs[v]:
                if att not in dataset.variables[v].attrs or force_profile:
                    value = attrs[v][att]
                    if value is None:
                        continue
                    dataset.variables[v].attrs[att] = value

    def add_field_encoding(
            cls,
            dataset: 'xr.Dataset',
            attrs: Mapping[str, Any],
            force_profile: bool = False) -> None:
        """Add field encoding to the dataset from a attribute definition
        file.

        Args:
            attrs (dict): the field encoding attributes to add when saving the
                dataset
        """
        # add attributes
        # overrides previous attribute values!!
        for v in attrs:
            if v not in dataset.variables:
                logging.warning(
                    'Field {} not found in the dataset to save. Skipping'
                    .format(v)
                )
                continue
            for att in attrs[v]:
                if att not in dataset.variables[v].encoding or force_profile:
                    value = attrs[v][att]
                    if att == 'dtype':
                        att = C_DTYPE
                    if value is None:
                        continue
                    dataset.variables[v].encoding[att] = value

    @property
    def collection_id(self) -> str:
        """return the identifier of the product collection"""
        return self.dataset.cb.collection_id

    def get_naming_authority(self) -> str:
        return self.dataset.cb.naming_authority
