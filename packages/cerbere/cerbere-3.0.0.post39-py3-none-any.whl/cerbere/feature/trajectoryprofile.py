# -*- coding: utf-8 -*-
"""
Feature class for the section observation pattern (a time series of profiles).
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

from cerbere.feature.feature import Feature

__all__ = ['TrajectoryProfile']


class TrajectoryProfile(Feature):
    """
    Feature class for the section observation patterns.

    A :class:`~cerbere.feature.section.Section` feature is defined by
    geolocation coordinates field: ``lon(profile)``, ``lat(profile)``,
    ``time(profile)``, ``depth/alt (profile, z)``, all having a single
    geolocation dimension: ``profile`` (except ``z`` for Z axis coordinate).
    """
    _feature_geodimnames = 'profile', 'z',

    def __init__(self, *args, **kwargs):
        super(TrajectoryProfile, self).__init__(*args, **kwargs)

        # CF specific attrs and vars for profile feature
        self._std_dataset.attrs['featureType'] = 'TrajectoryProfile'

        # mandatory coordinates
        for _, v in self._std_dataset.data_vars.items():
            v.attrs['coordinates'] = 'time lat lon z'

    def get_geocoord_dimnames(
            self, fieldname: str, *args, **kwargs) -> Tuple[str, ...]:
        if fieldname in ['lat', 'lon', 'time']:
            return 'profile',
        else:
            return 'profile', 'z',
