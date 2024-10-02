# -*- coding: utf-8 -*-
"""
Feature classes for grid observation patterns
"""
import copy
import inspect
import typing as T
import warnings

import xarray as xr
from xarray.core.utils import either_dict_or_kwargs

import cerbere
from cerbere.feature.cbasefeature import BaseFeature


__all__ = ['Grid']


# Plate Carree projection as default (regular isolat, isolon)
DEFAULT_PROJECTION = xr.DataArray(
    data=0,
    attrs={
        'grid_mapping_name': "latitude_longitude",
        'longitude_of_prime_meridian': 0.0,
        'semi_major_axis': 6378137.0,
        'inverse_flattening': 298.257223563}
)


class Grid(BaseFeature):
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
    cdm_data_type = 'grid'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': [('X', 'Y'), ('X',)],
        'latitude': [('X', 'Y'), ('Y',)],
        'time': [('T',), ('X', 'Y',)],
        'vertical': ('Z',),
        'data': [('X', 'Y'), ('T', 'X', 'Y')]
    }
    # optional axes for the feature
    cf_optional_axes = ['vertical']

    def nearest(self, lon, lat, z=None) -> xr.Dataset:
        # @TODO
        pass

    def inearest(self, lon, lat, z=None) -> T.Tuple[int]:
        # @TODO
        pass

    @classmethod
    def check_feature(cls, dataset: xr.Dataset) -> bool:
        cfdst = dataset.cb.cfdataset

        if cfdst.cb.cdm_data_type is not None and \
                cfdst.cb.cdm_data_type.lower() != cls.cdm_data_type:
            return False

        # check grid mapping parameters
        if dataset.cb.grid_mapping is None:
            warnings.warn(
                'No grid mapping parameters in dataset',
                cerbere.CWarning)

        if cfdst.cb.grid_mapping is not None:
            return True

        # check lat/lon are axes and two-dimensional
        for coordname in ['lon', 'lat']:
            if len(cfdst[coordname].dims) == 1:
                return
        if set(cfdst['lon'].dims) != set(cfdst['lat'].dims):
            return

        # check provided axes if any
        if (cfdst.cb.X is not None
                and cfdst.cb.X.name == cfdst.cb.longitude.name):
            return
        if (cfdst.cb.Y is not None
                and cfdst.cb.Y.name == cfdst.cb.latitude.name):
            return

        # time is unidimensional or (X, Y)
        if (len(cfdst.time.dims) != 1 and
                set(cfdst.time.dims) != {cfdst.cb.X.name, cfdst.cb.Y.name}):
            return


    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[BaseFeature]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if (cfdst.cb.cdm_data_type is not None
                and not cls._unexpected_cdm_data_type(cfdst)):
            return Grid

        # check horizontal axes are defined or at least some mapping
        if cfdst.cb.X is None and cfdst.cb.Y is None:
            if cfdst.cb.grid_mapping is None or cfdst.cb.grid_mapping_name:
                return

        if (cfdst.cb.cf_axis_dims.get('X') is None
                or cfdst.cb.cf_axis_dims.get('Y') is None):
            return
        elif  cfdst.cb.cf_axis_dims['X'] == cfdst.cb.cf_axis_dims['Y']:
            return

        # time is unidimensional or (X, Y)
        if (len(cfdst.time.dims) != 1 and
                set(cfdst.time.dims) != {cfdst.cb.X.name, cfdst.cb.Y.name}):
            return

        return Grid

    @classmethod
    def cerberize(
            cls,
            dataset: xr.Dataset,
            force_reorder: bool = True,
            instance_class: 'BaseFeature' = None
    ) -> xr.Dataset:
        cfdst = super().cerberize(dataset, force_reorder, instance_class)

        # add missing default mapping for cylindrical grids
        if dataset.cb.grid_mapping is None and cls._is_cylindrical(dataset):
            cfdst['crs'] = DEFAULT_PROJECTION

        # add mapping information to data variables
        if cfdst.cb.grid_mapping is not None:
            for v in cfdst.data_vars:
                if cfdst.cb.cf_axis_dims['X'] in cfdst[v].dims \
                        and cfdst.cb.cf_axis_dims['Y'] in cfdst[v].dims \
                        and 'grid_mapping' not in cfdst[v].attrs:
                    cfdst[v].attrs['grid_mapping'] = cfdst.cb.grid_mapping.name

        # squeeze time dimension in non-coordinate fields
        ctime = cfdst.time.copy()
        if 'time' in cfdst.dims and cfdst.sizes['time'] <= 1:
            cfdst = cfdst.squeeze(dim='time')
        cfdst.coords['time'] = ctime

        # Unidata CDM feature type
        if cls._is_cylindrical(cfdst):
            cfdst.attrs['cdm_data_type'] = 'grid'
        else:
            cfdst.attrs['cdm_data_type'] = cls.cdm_data_type

        return cfdst

    @classmethod
    def _is_cylindrical(cls, dataset) -> bool:
        # check lat/lon are axes and unidimensional
        if dataset.cb.X is None or dataset.cb.Y is None:
            return False

        if (dataset.cb.X.name != dataset.cb.longitude.name or
                dataset.cb.Y.name != dataset.cb.latitude.name):
            return False

        return True

    def is_cylindrical(self) -> bool:
        return self._is_cylindrical(self.dataset)

    def is_circular(self, precision: int = 3) -> bool:
        """Return True if the grid is cylindrical and False otherwise."""
        if not self.is_cylindrical():
            return False

        return (
            ((self.ds.lon[0] - self.ds.lon[-1]) % 360.).round(precision) ==
            ((self.ds.lon[1] - self.ds.lon[0]) % 360.) .round(precision))

    def isel(
            self,
            indexers: T.Any = None,
            circularity: bool = True,
            **kwargs
    ) -> T.Any:
        """
        shortcut for cerbere ds.cb.isel method but returns the result
        wrapped into a Feature object of the same class as the current object

        Parameters
        ----------
        circularity : bool
            in case of negative slices in the longitude axis, combine
            westward and eastward slices apart from the start longitude axis.
            True by default and overrides padding if set.
        """
        # separate indexer kargs from isel other kwargs
        isel_signature = inspect.getfullargspec(self.ds.cb.isel).args
        isel_kwargs = {k: v for k, v in kwargs.items() if k in isel_signature}
        indx_kwargs = {k: v for k, v in kwargs.items() if k not in
                       isel_signature}
        indexers = either_dict_or_kwargs(
            copy.copy(indexers), indx_kwargs, "isel")

        if not self.is_cylindrical() and circularity:
            # can not be applied to non cylindrical grids
            circularity = False

        if (not circularity
                or not self.is_circular()
                or 'lon' not in indexers
                or not isinstance(indexers['lon'], slice)):
            return self.__class__(self.ds.cb.isel(**indexers, **isel_kwargs))

        lon_slice = indexers.pop('lon')
        if lon_slice.start >= 0 and lon_slice.stop < self.ds.lon.size:
            # no split necessary
            return self.__class__(self.ds.cb.isel(
                {**indexers, **{'lon': lon_slice}}, **isel_kwargs))

        if lon_slice.start < 0 and lon_slice.stop > self.ds.lon.size:
            raise ValueError(f'slice {lon_slice} can not self wrap over a grid')

        if lon_slice.start < 0:
            lon_slice = [
                slice(self.ds.lon.size + lon_slice.start, self.ds.lon.size),
                slice(0, lon_slice.stop)]
        else:
            lon_slice = [
                slice(lon_slice.start, self.ds.lon.size),
                slice(0, lon_slice.stop - self.ds.lon.size)]

        return self.__class__(xr.concat(
            [self.ds.cb.isel(
                **{**indexers, **{'lon': lon_slice[0]}}, **isel_kwargs),
             self.ds.cb.isel(
                 **{**indexers, **{'lon': lon_slice[1]}}, **isel_kwargs)],
            dim='lon'))





#
# class CylindricalGrid(Grid):
#     """
#     Cylindrical lat/lon grid.
#     """
#     cdm_data_type = 'grid'
#
#     # the expected shape of the coordinates and variables, as defined by CF
#     # convention (CF 1.11, Table 9.1)
#     cf_canonical_dims = {
#         'longitude': ('X',),
#         'latitude': ('Y',),
#         'time': [('T',), ('X', 'Y',)],
#         'vertical': ('Z',),
#         'data': ('X', 'Y',)
#     }
#     # optional axes for the feature
#     cf_optional_axes = ['vertical']
#
#     def nearest(self, lon, lat, z=None) -> xr.Dataset:
#         # @TODO
#         if z is None:
#             return self.dataset.cf.sel(lon=lon, lat=lat, method='nearest')
#
#         z_coord = self.dataset.cf.axis_coordname('Z')
#         return self.dataset.cf.sel(
#             **{'lon': lon, 'lat': lat, z_coord: z}, method='nearest')
#
#     def inearest(self, lon, lat, z=None) -> T.Tuple[int]:
#         # @TODO
#         pass
#
#     @classmethod
#     def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[BaseFeature]:
#
#         cfdst = dataset.cb.cfdataset
#
#         # check Unidata CDM' feature type
#         if cfdst.cb.cdm_data_type is not None and \
#                 cfdst.cb.cdm_data_type.lower() != cls.cdm_data_type:
#             return
#
#         # check lat/lon are axes and unidimensional
#         for coordname in ['lon', 'lat']:
#             if len(cfdst[coordname].dims) != 1:
#                 return
#         if set(cfdst['lon'].dims) == set(cfdst['lat'].dims):
#             return
#
#         # check provided axes if any
#         if (cfdst.cb.X is not None
#                 and cfdst.cb.X.name != cfdst.cb.longitude.name):
#             return
#         if (cfdst.cb.Y is not None
#                 and cfdst.cb.Y.name != cfdst.cb.latitude.name):
#             return
#
#         # time is unidimensional or (lat, lon)
#         if (len(cfdst.time.dims) != 1 and
#                 set(cfdst.time.dims) != {cfdst.cb.X.name, cfdst.cb.Y.name}):
#             return
#
#         return CylindricalGrid
