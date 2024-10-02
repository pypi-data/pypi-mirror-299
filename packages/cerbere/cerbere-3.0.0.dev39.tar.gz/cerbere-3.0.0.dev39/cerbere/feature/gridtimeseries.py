# -*- coding: utf-8 -*-
"""
Feature classes for time ordered series of grid observation patterns
"""
from __future__ import absolute_import, division, print_function

import datetime
from typing import Tuple, Union

import numpy as np
import xarray as xr

from cerbere.feature.feature import Feature
from cerbere.feature.grid import CylindricalGrid, Grid, Projection
from cerbere.feature.trajectory import Trajectory

__all__ = ['GridTimeSeries', 'CylindricalGridTimeSeries']


class GridIterator:
    """Iterator for looping over a the grids of the time series"""

    def __init__(self, gridtimeseries):
        self.gridtimeseries = gridtimeseries
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.gridtimeseries.get_times()):
            raise StopIteration
        self.index = self.index + 1
        return self.gridtimeseries.extract_grid(self.index - 1)


class GridTimeSeries(Feature):
    """Class implementing a time series of grids


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
    cdm_data_type = 'grid'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'X': ('X'),
        'Y': ('Y'),
        'T': ('T'),
        'data': ('T', 'X', 'Y')
    }

    def __init__(self,
                 *args,
                 projection=Projection(),
                 **kwargs
                 ):
        # projection parameters
        self.projection = projection

        # create feature
        super(GridTimeSeries, self).__init__(
            *args,
            **kwargs
        )

    def __iter__(self):
        """Returns the iterator"""
        return GridIterator(self)

    @property
    def _grid_class(self):
        return Grid


    # def time2t(self, time: 'datetime.datetime'):
    #     """Get the index of the closest time step to the requested time
    #
    #     Args:
    #         time: the time of the closest time step sought in the series
    #     """
    #     numtime = date2num(time, self.get_time_units())
    #     return min(numpy.abs(self.get_times() - numtime).argmin(),
    #                len(self.get_times()) - 1
    #                )

    # def add_grid(self, grid, step=None):
    #     """Add or update a time step to a grid time series.
    #
    #     If the time step already exists, the corresponding values will be
    #     replaced.
    #
    #     Args:
    #         step (int): specify directly the index whithin the time series
    #             where to insert the grid (replacing the current values). If
    #             None, the time of the grid is used to search for the
    #             corresponding index within the time series.
    #     """
    #     time = num2date(grid.get_times()[0], grid.get_time_units())
    #     logging.debug("Source grid time : %s", time)
    #     epsilon = 1
    #     if step is None:
    #         step = 0
    #         steptime = num2date(self.get_times()[step],
    #                             self.get_time_units()
    #                             )
    #         while abs(time - steptime).total_seconds() > epsilon:
    #             step += 1
    #     if step >= len(self.get_times()):
    #         raise Exception('Time not found')
    #     else:
    #         logging.debug('Index in time series : %d', step)
    #         # CASE 1 : time step already exists => update
    #         # check if variable (and corresponding record) already exists
    #         for fieldname in grid.get_fieldnames():
    #             logging.debug('fieldname %s', fieldname)
    #             data = grid.get_values(fieldname)
    #             if self.has_field(fieldname):
    #                 logging.debug('gridtimeserie field already exist')
    #                 logging.debug("ADDING %s %s", fieldname, step)
    #                 field = self.get_field(fieldname)
    #                 logging.debug('field %s', field)
    #                 field._values[step, :, :] = data
    #             else:
    #                 logging.debug(
    #                     '[gridtimeserie] field %s doesnt exist yet in ts', fieldname)
    #                 field_to_add = grid.get_field(fieldname)
    #                 self.add_field(field_to_add)
    #     return



    def grid(self, step: Union[int, 'datetime.datetime', 'np.datetime64']):
        """Extract a grid from a grid time series

        Args:
            step: the grid to extract is defined either by :
                * a time step index (int)
                * a time as a datetime or numpy datetime64

        Return:
            :class:`Grid`: extracted grid.
        """
        if isinstance(step, int):
            grid = self.to_xarray().isel(time=step)
            if 'time' not in grid.time.dims:
                grid.coords['time'] = grid.time.expand_dims(time=1)
            return self._grid_class(grid)

        elif isinstance(step, (datetime.datetime, np.datetime64)):
            step = np.datetime64(step)
            grid = self.to_xarray().sel(time=[step])
            if 'time' not in grid.time.dims:
                grid.coords['time'] = grid.time.expand_dims(time=1)
            return self._grid_class(grid)


    def is_unique_grid_time(self):
        """
        Return True if a unique time is associated with the grid
        (like in L4 products), False if there is time value per pixel
        (like in L3)
        """
        dims = self.get_geolocation_field('time').dimensions.values()[0]
        return (dims == 1)


class CylindricalGridTimeSeries(GridTimeSeries):
    def __init__(self,
                 *args,
                 **kwargs
                 ):
        """
        Time series of cylindrical lat/lon grids.
        """
        # create feature
        super(CylindricalGridTimeSeries, self).__init__(
            *args,
            **kwargs
        )

    @property
    def _feature_geodimnames(self) -> Tuple[str, ...]:
        return 'time', 'lat', 'lon'

    @property
    def _grid_class(self):
        return CylindricalGrid

    def get_geocoord_dimnames(self, fieldname: str, values) -> Tuple[str, ...]:
        if fieldname in ['depth', 'height']:
            if len(values.shape) != 1:
                raise ValueError('z coordinate must be one-dimensional')
            return 'z',
        elif fieldname == 'time':
            if len(values.shape) != 1:
                raise ValueError(
                    'time coordinate must be one or two dimensional'
                )
            return 'time',
        else:
            return 'time', 'lat', 'lon',

    def trajectory(self, trajectory, **kwargs):
        """
        Extract the values along the provided trajectory.

        Args:
            Any args to xarray `:func:interp` function can be used here.
        """
        xtraj = trajectory._cfdataset
        return Trajectory(self._std_dataset.interp(
            lat=xtraj.lat,
            lon=xtraj.lon,
            time=xtraj.time,
            method='nearest'
        ))
