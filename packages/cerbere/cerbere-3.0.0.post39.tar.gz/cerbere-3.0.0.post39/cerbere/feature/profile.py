# -*- coding: utf-8 -*-
"""
Feature class for the profile observation pattern.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

import xarray as xr

from cerbere.feature.feature import Feature

__all__ = ['Profile']


class Profile(Feature):
    """
    Feature class for the profile observation patterns.

    A :class:`~cerbere.feature.profile.Profile` feature is defined by
    geolocation coordinates field: ``lon(profile)``, ``lat(profile)``,
    ``time(profile)``, ``z(profile, z)``, all having a single geolocation
    dimension: ``profile``.
    """
    _instance_dimname = 'profile'
    _feature_geodimnames = 'z',

    def __init__(self, *args, **kwargs):
        super(Feature, self).__init__(*args, **kwargs)

        # CF specific attrs and vars for profile feature
        self._std_dataset['profile'] = xr.DataArray(
            dims=(),
            attrs={'cf_role': 'profile_id'}
        )
        self._std_dataset.attrs['featureType'] = 'profile'
        for _, v in self._std_dataset.data_vars.items():
            v.attrs['coordinates'] = 'time lat lon z'

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height']:
            return 'z',
        else:
            return ()
