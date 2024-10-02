# -*- coding: utf-8 -*-
"""
Base class for any `cerbere` dataset. Built as a wrapper around a
:class:`~xarray.Dataset` object.
"""
import datetime
import logging
import os
import warnings
from pathlib import Path
from typing import Any, Dict, Hashable, List, Mapping, Optional, Tuple, Union
import typing as TP

import numpy as np
import pandas as pd
import shapely.geometry
import xarray as xr

from scipy.ndimage import find_objects, label, binary_dilation

import cerbere
from cerbere.accessor.cerberize import (
    _cerberize, CB_CERBERIZED, CB_COORDS, CB_AXIS_DIMS, CB_AXIS_COORDS,
    CB_INSTANCE_DIMS, CB_INSTANCE_COORDS, guess_cf_aux_coords)
import cerbere.cfconvention as cf
import cerbere.accessor.matching as match
from cerbere.exceptions import CoordinateError
from cerbere.accessor.netcdf import to_netcdf
from cerbere.feature.cdiscretefeature import DiscreteFeature


@xr.register_dataset_accessor("cb")
class DatasetAccessor:
    """
    """
    def __init__(self, xarray_obj):
        self._orig_dataset = None
        self._cfdataset = xarray_obj

        try:
            if xarray_obj.encoding.get(CB_CERBERIZED, False):
                return
        except AttributeError:
            pass

        # cached properties
        self._cfdataset.encoding[CB_CERBERIZED] = False

        # cerberize by guessing
        self.cerberize()

    def isel(
            self,
            indexers: Any = None,
            padding: bool = False,
            broadcast_coords: List[str] = None,
            prefix: Optional[str] = None,
            **kwargs: Any):
        """

        Args:
            indexers:
            padding:
            broadcast_coords:
            prefix:
            **kwargs:

        Returns:

        """
        if padding is False and broadcast_coords is None:
            subs = self.cfdataset.isel(indexers, **kwargs)
        else:
            if broadcast_coords is not None:
                for c in broadcast_coords:
                    if c not in self.cfdataset.coords:
                        raise ValueError(
                            f'{c} is not a coordinate, broadcast along this '
                            f'dimension is forbidden.'
                        )

            isel_args = kwargs.copy()
            isel_args.update(
                {'padding': padding, 'broadcast_coords': broadcast_coords})

            subs = xr.Dataset(
                attrs=self._cfdataset.attrs,
                data_vars={
                    _: self._cfdataset[_].cb.isel(indexers, **isel_args)
                    for _ in self._cfdataset.data_vars})
            # add missing coords
            for coord in self._cfdataset.coords:
                if coord not in subs.coords:
                    subs.coords[coord] = self._cfdataset[coord].cb.isel(
                        indexers, **isel_args)

            subs.encoding.update(self._cfdataset.encoding.copy())

        # prefix the output variables
        if prefix:
            subs = subs.rename({_: f'{prefix}_{_}' for _ in subs.data_vars})

        return subs

    @property
    def cfdataset(self) -> xr.Dataset:
        """Returns a CF normalized version of the dataset."""
        if self._cfdataset is None:
            # default standardization - may not be enough for some products
            # that have more unusual none-conformity
            self.cerberize()
        return self._cfdataset

    def is_cerberized(self):
        return self._cfdataset.encoding.get(CB_CERBERIZED, False)

    def cerberize(
            self,
            dim_matching: Optional[Dict[str, str]] = None,
            coord_matching: Optional[Dict[str, str]] = None,
            attr_matching: Optional[Dict[str, str]] = None,
            axis_coordinates: Optional[Dict[str, str]] = None,
            **kwargs):
        """
        Args:
            coord_matching (dict): explicitly provides the matching between file
                native vars (keys) and their Cerbere/CF equivalent (values).
        """
        # back-up original version for encoding information
        # @TODO may have a memory imprint if some data copy occur - may be
        #  better to only save variable and global encoding
        self._orig_dataset = self._cfdataset.copy(deep=False)

        # harmonize dataset wrt cerbere CF & ACDD conventions
        self._cfdataset = _cerberize(
            self._cfdataset,
            dim_matching=dim_matching,
            coord_matching=coord_matching,
            attr_matching=attr_matching,
            axis_coordinates=axis_coordinates
        )


    @property
    def latitude(self) -> xr.DataArray:
        """"Latitude coordinate, as a DataArray"""
        return self._cfdataset['lat']

    @property
    def longitude(self) -> xr.DataArray:
        """"Longitude coordinate, as a DataArray"""
        return self._cfdataset['lon']

    @property
    def time(self) -> xr.DataArray:
        """"Time coordinate, as a DataArray"""
        return self._cfdataset['time']

    @property
    def vertical(self) -> TP.Optional[xr.DataArray]:
        """"Vertical coordinate (height or depth), as a DataArray"""
        try:
            return self._cfdataset[self.cf_coords['vertical']]
        except KeyError:
            return

    def _encoding_attr(self, value: str, category: str =None) -> str:
        if category is None:
            return self._cfdataset.encoding[value]
        return self._cfdataset.encoding[category][value]

    def _assign_coordinate(self, coord: str, data_var: xr.DataArray):
        pass

    # def _guess_cf_coord_lat(self) -> Hashable:
    #     """CF criteria for latitude (CF 1.11):
    #
    #     Variables representing latitude must always explicitly include the
    #     units attribute; there is no default value. The recommended value of
    #     the units attribute is the string degrees_north. Also accepted are
    #     degree_north, degree_N, degrees_N, degreeN, and degreesN.
    #
    #     Optionally, the latitude type may be indicated additionally by
    #     providing the standard_name attribute with the value latitude, and/or
    #     the axis attribute with the value Y.
    #
    #     Coordinates of latitude with respect to a rotated pole should be given
    #     units of degrees, not degrees_north or equivalents, because
    #     applications which use the units to identify axes would have no means
    #     of distinguishing such an axis from real latitude, and might draw
    #     incorrect coastlines, for instance.
    #     """
    #     return self._guess_cf_coord(self._cfdataset, 'lat')
    #
    # def _guess_cf_coord_lon(self) -> Hashable:
    #     """CF criteria for longitude (CF 1.11):
    #
    #     Variables representing longitude must always explicitly include the
    #     units attribute; there is no default value. The recommended value of
    #     the units attribute is the string degrees_east. Also accepted are
    #     degree_east, degree_E, degrees_E, degreeE, and degreesE.
    #
    #     Optionally, the longitude type may be indicated additionally by
    #     providing the standard_name attribute with the value longitude,
    #     and/or the axis attribute with the value X.
    #
    #     Coordinates of longitude with respect to a rotated pole should be given
    #     units of degrees, not degrees_east or equivalents, because applications
    #     which use the units to identify axes would have no means of
    #     distinguishing such an axis from real longitude, and might draw
    #     incorrect coastlines, for instance.
    #     """
    #     return self._guess_cf_coord(self._cfdataset, 'lon')
    #
    # def _guess_cf_coord_time(self) -> Hashable:
    #     """
    #     CF criteria for time coordinate (CF 1.11):
    #
    #     Variables representing reference time must always explicitly include
    #     the units attribute; there is no default value. The units attribute
    #     takes a string value formatted as per the recommendations in the
    #     [UDUNITS] package. The following excerpt from the UDUNITS documentation
    #      explains the time unit encoding by example:
    #
    #     "The specification seconds since 1992-10-8 15:15:42.5 -6:00 indicates
    #     seconds since October 8th, 1992 at 3 hours, 15 minutes and 42.5
    #     seconds in the afternoon in the time zone which is six hours to the
    #      west of Coordinated Universal Time (i.e. Mountain Daylight Time).
    #     The time zone specification can also be written without a colon using
    #     one or two digits (indicating hours) or three or four digits
    #     (indicating hours and minutes)."
    #
    #     The acceptable units for time are given by the UDUNITS package
    #      [UDUNITS]. The most commonly used of these strings (and their
    #      abbreviations) includes day (d), hour (hr, h), minute (min) and second
    #      (sec, s). Plural forms are also acceptable.
    #
    #     The reference date/time string (appearing after the identifier since)
    #     is required. It may include date alone, or date and time, or date, time
    #     and time zone. If the time zone is omitted the default is UTC, and if
    #     both time and time zone are omitted the default is 00:00:00 UTC.
    #
    #     A reference time coordinate is identifiable from its units string alone.
    #
    #     Optionally, the time coordinate may be indicated additionally by
    #     providing the standard_name attribute with an appropriate value, and/or
    #     the axis attribute with the value T.
    #
    #     Returns:
    #
    #     """
    #     return self._guess_cf_coord(self._cfdataset, 'time')
    #
    # def _guess_cf_coord_vertical(self) -> Hashable:
    #     return self._guess_cf_coord(self._cfdataset, 'vertical')

    @staticmethod
    def _verify_cf_axes(dst: xr.Dataset, axes: TP.Dict[str, TP.Hashable]):
        """To be a CF axis, the corresponding coordinate should be the only
        one depending on the axis dimension"""
        for axis in axes:
            # verify there is no other coordinate depending on this axis
            for coord in dst.cb.cf_coords:
                if coord.cb.axis != axis and axis in coord.dims:
                    raise cerbere.BadAxisError(
                        f'The axis dimension {axis} is used by different '
                        f'coordinate variables and therefore not be an axis '
                        f'dimension')
    #
    # def _guess_coord(self, axis: str) -> str:
    #     """Guess which variable is a given axis coordinate"""
    #     for c in self._cfdataset.coords:
    #         attrs = self._cfdataset.coords[c].attrs
    #         if 'axis' in attrs and attrs['axis'] == axis:
    #             return self._cfdataset.coords[c].name
    #     logging.debug(f'No {axis} coordinate found')
    #
    #     # try in variables
    #     for c in self._cfdataset.data_vars:
    #         attrs = self._cfdataset.data_vars[c].attrs
    #         if 'axis' in attrs and attrs['axis'] == axis:
    #             return self._cfdataset.data_vars[c].name
    #     logging.debug(f'No {axis} coordinate found')
    #
    # def _guess_t_coord(self) -> str:
    #     """Guess which variable is a T axis coordinate"""
    #     return self._guess_coord('T')
    #
    # def _guess_x_coord(self) -> str:
    #     """Guess which variable is a X axis coordinate"""
    #     x_coord = self._guess_coord('X')
    #     if x_coord is not None:
    #         return x_coord
    #
    #     if 'lon' in self._cfdataset.coords and \
    #             len(self._cfdataset.lon.dims) < 2:
    #         return 'lon'
    #
    # def _guess_y_coord(self) -> str:
    #     """Guess which variable is a Y axis coordinate"""
    #     y_coord = self._guess_coord('Y')
    #     if y_coord is not None:
    #         return y_coord
    #
    #     if 'lat' in self._cfdataset.coords and \
    #             len(self._cfdataset.lon.dims) < 2:
    #         return 'lat'
    #
    # def _guess_z_coord(self) -> str:
    #     """Guess which variable is a Z axis coordinate"""
    #     return self._guess_coord('Z')

    def set_as_z(self, fieldname: str, positive=None):
        """Set a field as representing the Z coordinate"""
        # add Z axis CF attribute
        self._cfdataset[fieldname].attrs['axis'] = 'Z'
        if positive is not None:
            if 'positive' in self._cfdataset[fieldname].attrs:
                logging.warning(
                    'positive attribute already defined and will be overriden '
                    'by the new value'
                )
                self._cfdataset[fieldname].attrs['positive'] = positive

        # remove previous Z axis (only one coordinate can be Z axis)
        for v in self._cfdataset.variables:
            if ('axis' in self._cfdataset[v].attrs and
                    self._cfdataset[v].attrs['axis'] == 'Z'):
                self._cfdataset[v].attrs.pop('axis')
                break

        # set as coordinate
        self._cfdataset = self._cfdataset.set_coords([fieldname])

    def __str__(self):
        result = 'Dataset: \nCF Spatiotemporal Dims :\n'
        for dim, dsize in self.cf_dims.items():
            result = result + '   .\t{} : {}\n'.format(dim, dsize)

        result = result + 'Other Dims :\n'
        for dim, dsize in self._cfdataset.dims.items():
            if dim in self.cf_dims:
                continue
            result = result + '   .\t{} : {}\n'.format(dim, dsize)

        result = result + 'CF Spatiotemporal Coordinates :\n'
        # TODO replace geocoordnames
        for coord in self.geocoordnames:
            result = result + '   .\t{}  ({})\n'.format(
                coord,
                ', '.join(
                    [(str(k) + ': ' + str(v))
                     for k, v in self._cfdataset[coord].sizes.items()]))

        result = result + 'Other Coordinates :\n'
        for coord in self.coordnames:
            if coord in self.geocoordnames:
                continue
            result = result + '   .\t{}  ({})\n'.format(
                coord,
                ', '.join(
                    [(str(k) + ': ' + str(v))
                     for k, v in self._cfdataset[coord].sizes.items()]
                )
            )

        result = result + 'Data :\n'
        for field in self._cfdataset.data_vars:
            result = result + '   .\t{}  ({})\n'.format(
                field,
                ', '.join(
                    [(str(k) + ': ' + str(v))
                     for k, v in self._cfdataset[field].sizes.items()]
                )
            )

        result = result + 'Global Attributes :\n'
        for attr in self.cfdataset.attrs:
            result += f'   .\t{attr}\t{str(self.cfdataset.attrs[attr])}\n'

        return result

    def is_empty(self) -> bool:
        """Returns True if the dataset object contains no data yet"""
        return self._cfdataset.equals(xr.Dataset())

    @property
    def basename(self) -> str:
        """Return the basename of the file storing the dataset"""
        return Path(self.url).name

    @property
    def filesize(self) -> int:
        """The dataset file size, in octets"""
        return os.path.getsize(self.url)

    @property
    def file_creation_date(self) -> 'datetime.datetime':
        """The date the dataset file was generated"""
        return datetime.datetime.fromtimestamp(os.path.getctime(self.url))

    def has_coord(self, coord: Hashable) -> bool:
        """Return True if the coordinate field is defined"""
        return coord in self._cfdataset.coords

    # @property
    # def dimnames(self) -> Tuple[Hashable]:
    #     """Tuple of the dataset's dimension names"""
    #     return tuple(self.cfdataset.sizes.keys())
    #
    # @property
    # def dimsizes(self) -> Tuple[int]:
    #     """Tuple of the dataset's dimension sizes"""
    #     return tuple(self.cfdataset.dims.values())

    @property
    def _varnames(self) -> List[Hashable]:
        """List of the names of all the fields (including coordinates) of the
        dataset.
        """
        return list(self._cfdataset.variables.keys())

    @property
    def cf_coords(self) -> TP.Dict[str, str]:
        """Return the spatiotemporal coordinate variables

        Return:
          dict: a dictionary where keys are the CF spatiotemporal coordinates (
          among longitude, latitude, vertical, time) and values are the
          coordinate names for these axes.
        """
        if not self.is_cerberized():
            self.cerberize()
        return self._cfdataset.encoding.get(CB_COORDS)

    @property
    def cf_axis_coords(self) -> TP.Dict[str, str]:
        """Return the spatiotemporal axis coordinate variables.

        The axis coordinates may be different from the coordinates,
        for instance in curvilinear grids having projection X and Y
        axis coordinates.

        Return:
          dict: a dictionary where keys are the CF axes (X, Y, Z, T) and
            values the coordinate names for these axes.
        """
        if not self.is_cerberized():
            self.cerberize()
        return self._cfdataset.encoding.get(CB_AXIS_COORDS)

    @staticmethod
    def _find_axis_coord(
            dst: xr.Dataset, axis: str) -> TP.Optional[TP.Hashable]:
        """Return the name of the spatiotemporal coordinate associated
        with a given CF axis, based on the CF axis attribute.

        Args:
            dst: the dataset in which to search the axis coordinate
            axis: axis name among 'X', 'Y', 'T', 'Z'
        """
        if axis not in cf.CF_AXIS:
            raise cerbere.AxisError(
                '{} is not a geolocation coordinate'.format(axis))

        axis_coord = [
            coord for coord in dst.variables
            if dst[coord].attrs.get('axis') == axis]

        if len(axis_coord) == 0:
            raise cerbere.MissingAxisError(
                f'No coordinate found for axis: {axis}')
        if len(axis_coord) != 1:
            raise cerbere.BadAxisError(
                f'Too many coordinates found for axis: {axis}: {axis_coord}. '
                f'There can be only one coordinate for a given axis. This file '
                f'or dataset should be fixed first.')

        return axis_coord[0]

    def rename_cf_axis_coord(self, axis: str, name: str):
        """
        Rename an axis coordinate.

        Update cerbere internals at the same time to maintain encoding
        consistency.

        Args:
            axis: axis coordinate to rename, among 'X', 'Y', 'Z' or 'T'
            name: new name for the axis coordinate
        """
        if axis not in cf.CF_AXIS:
            raise cerbere.AxisError(f'Illegal axis {axis}')
        if axis in self.cf_axis_coords:
            raise cerbere.AxisError(f'{axis} is not an axis coordinate')
        prev_name = self.cf_axis_coords.pop(axis)
        self.cf_axis_coords[axis] = name
        if prev_name in self.cf_coords.values():
            coord = {self.cf_coords[_]: _ for _ in self.cf_coords}[prev_name]
            self.cf_coords[coord] = name

    def rename_cf_axis_dim(self, axis: str, name: str):
        """
        Rename an axis dimension.

        Update cerbere internals at the same time to maintain encoding
        consistency.

        Args:
            axis: axis dimension to rename, among 'X', 'Y', 'Z' or 'T'
            name: new name for the axis dimension
        """
        self.cf_axis_dims[axis] = name

    def set_axis(self, name: str, axis: str):
        """Set a variable as a CF axis.

        Args:
            name: name of the variable to set as an axis
            axis: value of the axis
        """
        if axis not in cf.CF_AXIS:
            raise cerbere.AxisError(f'Illegal axis {axis}')

        # verify there is no variable with this axis already
        axis_vars = set([
            _ for _ in self._cfdataset.variables
            if self._cfdataset[_].attrs.get('axis') == axis]) - {name}

        if len(axis_vars) > 0:
            logging.warning(
                f'The following variable(s) were set as {axis} axis: '
                f'{axis_vars}. They will be unset by this action.'
            )
            if axis in self.cf_axis_coords:
                self.cf_axis_coords.pop(axis)
            for v_axis in axis_vars:
                self._cfdataset[v_axis].attrs.pop('axis')
                if v_axis in self._cfdataset.coords:
                    self._cfdataset = self._cfdataset.reset_coords(v_axis)

        self._cfdataset[name].attrs['axis'] = axis
        self.cf_axis_coords[axis] = name
        self._cfdataset = self._cfdataset.set_coords([name])

        # re-cerberize to update internal encoding
        self._cfdataset = _cerberize(self._cfdataset)

    def _cf_axis(self, axis: str):
        """Return the corresponding dimension name for a given axis"""
        if not self.is_cerberized():
            self.cerberize()
        return self._cfdataset.encoding.get('_cb_axes').get(axis)

    @property
    def X(self) -> Optional[xr.DataArray]:
        """Return the X axis coordinate variable"""
        if self.cf_axis_coords.get('X') is None:
            return
        return self._cfdataset[self.cf_axis_coords['X']]

    @property
    def Y(self) -> Optional[xr.DataArray]:
        """Return the Y axis coordinate variable"""
        if self.cf_axis_coords.get('Y') is None:
            return
        return self._cfdataset[self.cf_axis_coords['Y']]

    @property
    def T(self) -> Optional[xr.DataArray]:
        """Return the T (time) axis coordinate variable"""
        return self._cfdataset[self.cf_axis_coords['T']]

    @property
    def Z(self) -> Optional[xr.DataArray]:
        """Return the Z (vertical) axis coordinate variable"""
        return self._cfdataset[self.cf_axis_coords['Z']]

    @property
    def cf_axis_dims(self) -> Mapping[str, str]:
        """Return the mapping from CF spatiotemporal axis (X, Y, Z,
        T) to the dimension names in the dataset
        """
        return self._cfdataset.encoding[CB_AXIS_DIMS]

    @property
    def cf_instance_dims(self) -> List[str]:
        """Return the instance axis dimensions of a feature collection
        """
        return self._cfdataset.encoding[CB_INSTANCE_DIMS]

    @property
    def cf_instance_coords(self) -> List[str]:
        """Return the instance axis coordinates of a feature collection
        """
        return self._cfdataset.encoding[CB_INSTANCE_COORDS]

    @property
    def cf_dims(self) -> Mapping[str, int]:
        """Return the mapping from CF spatiotemporal dimension names to lengths.
        """
        return {
            _: self._cfdataset.sizes[_]
            for _ in list(self._cfdataset.dims)
            if _ in self._cfdataset.encoding[CB_AXIS_DIMS].values()}

    @property
    def is_collection(self):
        return len(self.cf_instance_dims) > 0

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

    def clip(
            self,
            geometry: shapely.geometry.Polygon,
            masked: bool = False,
            continuity_threshold: int = 0,
            **kwargs) -> List[xr.Dataset]:
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
        # coarse search on geometry bounding box
        (lonmin, latmin, lonmax, latmax) = geometry.bounds

        # get spatial dimensions
        spatial_dims = list(self.cfdataset.coords['lat'].dims)
        for d in self.cfdataset.coords['lon'].dims:
            if d not in spatial_dims:
                spatial_dims.append(d)

        # coarse search on geometry bounding box
        lat = self.cfdataset.cb.latitude.cb.isel(
            broadcast_coords=[self.cfdataset.coords[_] for _ in spatial_dims],
            as_masked_array=False)
        lon = self.cfdataset.cb.longitude.cb.isel(
            broadcast_coords=[self.cfdataset.coords[_] for _ in spatial_dims],
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
            subsets.append(self.isel(dslices, **kwargs))

            if masked:
                raise NotImplementedError

        return subsets

    def get_location_by_value(self, field, value, **kwargs):
        """Return the indices and geolocation of a given value.

        If the value is not unique, the first one found is returned.
        """
        # TODO remove or update
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
        # TODO remove or update
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

    @property
    def bbox(self) -> 'shapely.geometry.Polygon':
        """The bounding box, e.g. the south/north and east/west
        limits of the feature.
        """
        if 'bbox' not in self.cfdataset.attrs:
            # calculate bbox automatically if not explicitely defined
            self.bbox = 'auto'
        return self.cfdataset.attrs['bbox']

    @bbox.setter
    def bbox(self,
             bbox: Union[str, tuple, shapely.geometry.Polygon] = 'auto'):
        """Set the bounding box of the feature

        Args:
            :class:`shapely.geometry.Polygon`: the bounding box. If None, it is
                estimated from the feature lat/lon.
        """
        if isinstance(bbox, tuple):
            warnings.warn(
                'bbox as a tuple is deprecated. Use shapely geometry.',
                FutureWarning
            )
            self.cfdataset.attrs['bbox'] = shapely.geometry.box(bbox)
        elif isinstance(bbox, shapely.geometry.Polygon):
            self.cfdataset.attrs['bbox'] = bbox
        elif bbox == 'auto':
            # look first at global attributes
            attrs = self.cfdataset.attrs
            limits = []
            for limit in ['lonmin', 'latmin', 'lonmax', 'latmax']:
                # check various geographical attribute styles
                for att in match.BBOX_CORNERS[limit]:
                    fatt = next((x for x in attrs if x == att), None)
                    if fatt is not None:
                        limits.append(attrs[fatt])
            if len(limits) == 4:
                self.cfdataset.attrs['bbox'] = shapely.geometry.box(*limits)

            # estimate from the lat/lon
            elif self.latitude is not None and self.longitude is not None:
                lats = self.latitude
                lons = self.longitude
                self.cfdataset.attrs['bbox'] = shapely.geometry.box(
                    lons.min(),
                    lats.min(),
                    lons.max(),
                    lats.max()
                )
            else:
                logging.warning('Could not infer bbox')
                self.cfdataset.attrs['bbox'] = None
        else:
            raise TypeError('Wrong type for bbox: {}'.format(type(bbox)))

    @property
    def wkt_bbox(self) -> str:
        """The bounding box in WKT format."""
        if self.bbox is not None:
            return self.bbox.wkt

    def save(self,
             path: Union[str, Path],
             profile: str = 'default_saving_profile.yaml',
             writer: str = None,
             force_profile: bool = False,
             keep_src_encoding: bool = False,
             **kwargs
             ):
        """
        Args:
            path (str, optional): save to a new file, whose path is provided in
                this argument. Raise an exception if the file already exists.
            profile (str, optional): path to a specific format profile to
                apply before saving (or default formatting profile is used).
            force_profile (bool, optional): force profile attribute values to
                supersede existing ones in dataset attributes.
            keep_src_encoding (bool): keep original dtype, _FillValue
                and scaling if any (through `add_offset` or `scale_factor`
                attributes) as in the source data.
        """
        if writer is not None:
            ds = cerbere.reader_class(writer).preprocess(self.cfdataset)
        else:
            ds = self.cfdataset.copy(deep=False)

        to_netcdf(
            path, ds, profile=profile,
            force_profile=force_profile,
            keep_src_encoding=keep_src_encoding, **kwargs)

    @property
    def collection_id(self) -> str:
        """return the identifier of the product collection"""
        if 'id' in self._cfdataset.attrs:
            return self._cfdataset.attrs['id']

    @property
    def naming_authority(self) -> str:
        if 'Conventions' in self._cfdataset.attrs:
            return self._cfdataset.attrs['Conventions']

    @property
    def product_version(self):
        """Return the product version"""
        if 'product_version' in self._cfdataset.attrs:
            return self._cfdataset.attrs['product_version']

    @property
    def url(self) -> Path:
        return Path(self._cfdataset.encoding.get('source'))

    @url.setter
    def url(self, value: Union[str, Path]):
        self._cfdataset.encoding['source'] = value

    def _time_coverage_from_coord(self):
        """Infer the dataset time coverage from its time coordinate.

        May cost some computation time and memory as the whole time
        coordinate will be loaded. It may be smarter to address this in a
        reader for a given dataset.
        """
        logging.warning(
            'loading the time coordinate in memory to extract the start and '
            'end time coverage')

        times = self._cfdataset.time
        if times.count() == 0:
            logging.warning('No valid time in dataset.')
            return

        # cache result
        start = pd.to_datetime(times.min(skipna=True).data)
        end = pd.to_datetime(times.max(skipna=True).data)
        # if len(times.dims) == 0:
        #     start = pd.to_datetime(times.min().data)
        #     end = pd.to_datetime(times.max().data)
        # else:
        #     start = pd.to_datetime(times[times.notnull()].min().values)
        #     end = pd.to_datetime(times[times.notnull()].max().values)

        self._cfdataset.attrs['time_coverage_start'] = start.to_pydatetime()
        self._cfdataset.attrs['time_coverage_end'] = end.to_pydatetime()

    def _time_coverage(
            self,
            boundary='time_coverage_start') -> datetime.datetime:
        if self._cfdataset.attrs.get(boundary) is None:
            # compute from time coordinate - may take some time
            self._time_coverage_from_coord()
        return self._cfdataset.attrs[boundary]

    @property
    def time_coverage_start(self) -> datetime.datetime:
        """Returns the first measurement time in the data.

        If the information is not available as an internal attribute, it will be
        computed (and cached) which may take some computation time as it
        required to read the values of the time coordinate.
        """
        return self._time_coverage('time_coverage_start')

    @time_coverage_start.setter
    def time_coverage_start(self, value: datetime.datetime):
        self._cfdataset.attrs['time_coverage_start'] = value

    @property
    def time_coverage_end(self) -> datetime.datetime:
        """Returns the last measurement time in the data.

        If the information is not available as an internal attribute, it will be
        computed (and cached) which may take some computation time as it
        required to read the values of the time coordinate.
        """
        return self._time_coverage('time_coverage_end')

    @time_coverage_end.setter
    def time_coverage_end(self, value: datetime.datetime):
        self._cfdataset.attrs['time_coverage_end'] = value

    @property
    def geospatial_bounds(self) -> str:
        return self._cfdataset.attrs.get('geospatial_bounds', None)

    @property
    def featureType(self) -> str:
        """the CF feature type of the data contained in the dataset"""
        return self._cfdataset.attrs.get('featureType', None)

    @property
    def cdm_data_type(self) -> str:
        """the Unidata Common Data Model feature type of the data contained in
        the dataset"""
        return self._cfdataset.attrs.get('cdm_data_type', None)

    @property
    def cf_role(self) -> Dict[str, str]:
        """Returns the name and role of the coordinates holding the cf role
        keyword"""
        return {v: self._cfdataset[v].attrs.get('cf_role')
                for v in self._cfdataset.variables}

    @property
    def cf_auxiliary_coords(self) -> TP.List[str]:
        """The spatiotemporal coordinates, among longitude, latitude,
        vertical or time, which depends on more than one spatiotemporal
        dimension"""
        return guess_cf_aux_coords(self._cfdataset).keys()

    @property
    def grid_mapping(self) -> TP.Union[xr.DataArray, TP.List[xr.DataArray]]:
        """Return the grid mapping variable(s)"""
        mvars = [_ for _ in self._cfdataset.data_vars
                 if self._cfdataset[_].attrs.get('grid_mapping_name')]

        if len(mvars) == 0:
            return

        if len(mvars) == 1:
            return self._cfdataset[mvars[0]]

        return [self._cfdataset[_] for _ in mvars]

    @property
    def grid_mapping_name(self) -> TP.Union[str, TP.List[str]]:
        """Return the grid mapping name"""
        mvars = self.grid_mapping
        if mvars is None:
            return

        if isinstance(mvars, list):
            return [
                _.attrs.get('grid_mapping_name') for _ in mvars]

        return mvars.attrs.get('grid_mapping_name')
