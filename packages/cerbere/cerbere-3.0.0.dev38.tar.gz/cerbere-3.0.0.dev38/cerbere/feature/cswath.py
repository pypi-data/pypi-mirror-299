# -*- coding: utf-8 -*-
"""
Class for the swath feature
"""
import typing as T
import warnings

import xarray as xr

import cerbere
from cerbere.feature.cbasefeature import BaseFeature
from cerbere.feature.cgrid import Grid


__all__ = ['Swath']


class Swath(Grid):
    """
    Feature class for representing a swath, a two-dimensional irregular grid
    along the satellite ground track.
    """
    cdm_data_type = 'swath'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': ('X', 'Y'),
        'latitude': ('X', 'Y'),
        'time': [('X', 'Y'), ('Y',)],
        'vertical': [('Z',), ('X', 'Y')],
        'data': ('X', 'Y')
    }

    # optional axes for the feature
    cf_optional_axes = ['vertical']

    # axis naming
    cb_axis_naming = {'X': 'across_track', 'Y': 'along-track'}

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
        if not set(cfdst['lon'].dims) == set(cfdst['lat'].dims) or not \
                (set(cfdst['lat'].dims) == set(cfdst['time'].dims) or
                 {cfdst.cb.cf_axis_dims['Y']} == set(cfdst['time'].dims)):
            return

        if cfdst.cb.vertical is not None and set(cfdst['lon'].dims) != set(
                cfdst.cb.vertical.dims):
            return

        if len(set(cfdst['lon'].dims)) != 2:
            return

        return Swath
