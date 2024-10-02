# -*- coding: utf-8 -*-
"""
Feature classes for grid observation patterns
"""
from typing import Tuple

import numpy as np
import xarray as xr

from .feature import Feature

__all__ = ['DEFAULT_PROJECTION', 'Projection', 'Grid', 'CylindricalGrid']


# Plate Carree projection as default (regular isolat, isolon)
DEFAULT_PROJECTION = (
    '+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +a=6378137 +b=6378137'
    ' +units=m'
)


class Projection(object):
    """Definition of a grid projection"""
    def __init__(self,
                 proj4_definition: str = DEFAULT_PROJECTION,
                 identifier: str = 'regular'
                 ):
        self.definition = proj4_definition
        self.identifier = identifier

    def is_cylindrical(self) -> bool:
        """True if the projection is cylindrical"""
        return self.identifier == 'regular'


class Grid(Feature):
    """
    Model class for the grid feature, ie a two-dimensional array on fixed
    projection, resolution and boundaries.

    A grid can be built from the ``content`` argument:
        * if None, the feature will undefined but can be updated later (for
          instance loading the content from a file with ``load`` method)
        * from the content of a file, providing a mapper class object
        * from an xarray dataset object
        * from a dictionary of coordinate and data fields. For coordinate
          fields, use only any of 'lat', 'lon', 'time', 'z' as keys.

          The coordinate fields can be provided as numpy arrays of values,
          :class:`cerbere.datamodel.field.Field` class objects, or
          :class:`xarray.DataArray` class objects.

          The lat and lon coordinate fields can also be provided as tuple
          (min, max, step): this is only for a regular grid. The values
          are automatically generated.

          The geophysical fields, in ``fields`` can be
          :class:`cerbere.datamodel.field.Field` class objects, or
          :class:`xarray.DataArray` class objects.

    .. code-block:: python

        from cerbere.feature.grid import Grid
        from cerbere.dataset.ncdataset import NCDataset

        ncf = NCDataset(url='SSS_SMOS_L3_Daily_0.5deg_CATDS_CECOS_2012.12.30_V02.nc')
        g = Grid(ncf)

    Args:
        content (xarray, mapper or dict of fields): the content from which to
            build the feature coordinates and data fields.

        attrs (dict): a dictionary of global attributes (as in a NetCDF file).
            Make use of the CF attributes. If the feature content is read from
            a file through a mapper, these attributes will be added to the
            existing the list of attributes already in the file (or replace the
            values of the existing attributes with the same name in the file).
            Use with caution in this context.
    """
    _required_dims = 'y', 'x',

    def __init__(self,
                 *args,
                 projection: 'Projection' = Projection(),
                 **kwargs
                 ):
        """
        """
        # projection parameters
        self.projection = projection

        # create feature
        super(Grid, self).__init__(
            *args,
            **kwargs
        )

        # squeeze time dimension in non-coordinate fields
        ctime = self._std_dataset.time.copy()
        if 'time' in self._std_dataset.dims:
            self._std_dataset = self._std_dataset.squeeze(dim='time')
        self._std_dataset.coords['time'] = ctime

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height', 'alt']:
            return 'z',
        elif fieldname == 'time':
            if len(values.shape) == 1:
                return 'time',
            else:
                return 'y', 'x'
        else:
            return 'y', 'x'

    def get_spatial_resolution(self):
        """Return the spatial resolution of the feature, in degrees"""
        if self.spatial_resolution is None:
            mapper = self.get_mapper()
            if mapper:
                return mapper.get_spatial_resolution_in_deg()
        else:
            return self.spatial_resolution



class CylindricalGrid(Grid):

    def __init__(self,
                 *args,
                 **kwargs
                 ):
        """
        Cylindrical lat/lon grid.
        """
        # create feature
        super(CylindricalGrid, self).__init__(
            *args,
            **kwargs
        )

    @property
    def _feature_geodimnames(self):
        return 'lat', 'lon',

    def get_geocoord_dimnames(self, fieldname, values):
        if fieldname in ['depth', 'height']:
            if len(values.shape) != 1:
                raise ValueError('z coordinate must be one-dimensional')
            return ('z',)
        elif fieldname == 'time':
            if len(values.shape) == 1:
                return ('time',)
            elif len(values.shape) == 2:
                return ('lat', 'lon',)
            else:
                raise ValueError(
                    'time coordinate must be one or two dimensional'
                )
        else:
            return ('lat', 'lon',)

    def closest_spatial_location(self, lon, lat):
        """Get closest dataset lat/lon location to given coordinates.

        Use pythagorian differences on lat/lon values so take the result with
        caution.

        Returns:
            A tuple with the indices and lon/lat of the closest point found.
        """
        idx_lon = np.abs(self.get_lon() - lon).argmin()
        idx_lat = np.abs(self.get_lat() - lat).argmin()

        loc = {'lat': idx_lat, 'lon': idx_lon}

        geoloc = (self.get_lon().flat[idx_lon], self.get_lat().flat[idx_lat])

        return loc, geoloc,
