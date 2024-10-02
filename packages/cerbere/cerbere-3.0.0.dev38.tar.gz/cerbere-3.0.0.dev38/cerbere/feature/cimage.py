# -*- coding: utf-8 -*-
"""
Class for the swath feature
"""
import typing as T
import logging
import warnings

import xarray as xr

import cerbere
from cerbere.feature.cbasefeature import BaseFeature
from cerbere.feature.cgrid import Grid


__all__ = ['Image']


class Image(BaseFeature):
    """
    Feature class for representing a image, a two-dimensional irregular grid
    along a satellite track, with one single time value associated.

    An image feature typically corresponds to a satellite "snapshot" like
    provided typically with a SAR (though technically it is more a swath) or a
    high resolution optical imager: a spatially limited swath section, so small
    that we don't need a time value for each pixel or even scan line. A single
    time value is enough to describe it, as if it was an instant snapshot.
    """
    cdm_data_type = 'curvilinear'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': ('X', 'Y',),
        'latitude': ('X', 'Y',),
        'time': ['()', ('T',)],
        'vertical': ('Z',),
        'data': ('X', 'Y',)
    }

    # optional axes for the feature
    cf_optional_axes = ['vertical']

    # axis naming
    cb_axis_naming = {'X': 'across_track', 'Y': 'along-track'}

    def cerberize(
            cls,
            dataset: xr.Dataset,
            force_reorder: bool = True,
            instance_class: 'BaseFeature' = None
    ) -> xr.Dataset:

        # squeeze time dimension in non-coordinate fields
        # ctime = self.dataset.time.copy()
        # if 'time' in self.dataset.dims:
        #     self.dataset = self.dataset.squeeze(dim='time')
        # self.dataset.coords['time'] = ctime

        return super().cerberize(dataset, force_reorder, instance_class)

    def check_feature(cls, dataset: xr.Dataset) -> bool:
        with warnings.catch_warnings(category=cerbere.CWarning):
            warnings.simplefilter("ignore")
            return Grid.check_feature(dataset)

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[BaseFeature]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_cdm_data_type(cfdst):
            return

        # check horizontal axes are defined or at least some mapping
        if cfdst.cb.X is not None or cfdst.cb.Y is not None:
            return

        if cfdst.cb.cf_axis_dims['X'] == cfdst.cb.cf_axis_dims['Y']:
            return

        # check lat/lon/time are two-dimensional and share the same
        # dimensions
        if set(cfdst['lon'].dims) != set(cfdst['lat'].dims):
            return

        # check time is one-dimensional and has only one single value
        if cfdst['time'].sizes != (1,) and cfdst['time'].dims[0] != 'time':
            return

        if cfdst.cb.vertical is not None and set(cfdst['lon'].dims) != set(
                cfdst.cb.vertical.dims):
            return
        if len(set(cfdst['lon'].dims)) != 2:
            return

        return Image
