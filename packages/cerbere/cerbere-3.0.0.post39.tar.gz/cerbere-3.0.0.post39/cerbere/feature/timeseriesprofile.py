# -*- coding: utf-8 -*-
"""
Feature class for the time series of profiles observation pattern.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

from cerbere.dataset.dataset import STANDARD_Z_FIELD
from cerbere.feature.feature import Feature


class TimeSeriesProfile(Feature):
    """
    Feature class for the time series of profiles observation pattern.

    A :class:`~cerbere.feature.timeseriesprofile.TimeSeriesProfile` feature is
    defined by geolocation coordinates field, , all having a single geolocation
    dimension: ``profile`` (except ``z`` for Z axis coordinate).
      * ``lon(profile)``
      * ``lat(profile)``
      * ``time(profile)``
      * ``depth/alt (profile, z)``
    """
    _feature_geodimnames = 'profile', 'z',

    def __init__(self, *args, **kwargs):
        super(TimeSeriesProfile, self).__init__(*args, **kwargs)

        # CF specific attrs and vars for profile feature
        self._std_dataset.attrs['featureType'] = 'timeSeriesProfile'

        # mandatory coordinates
        for _, v in self._std_dataset.data_vars.items():
            v.attrs['coordinates'] = 'time lat lon z'

    def get_geocoord_dimnames(
            self, fieldname: str, *args, **kwargs) -> Tuple[str, ...]:
        if fieldname in STANDARD_Z_FIELD or self.coords[fieldname].is_axis('Z'):
            return 'profile', 'z',
        else:
            return 'profile',


class UniZTimeSeriesProfile(Feature):
    """
    Feature class for the time series of profiles observation pattern, where z
    is unique and identical for each profile in the series.

    A :class:`~cerbere.feature.timeseriesprofile.TimeSeriesProfile` feature is
    defined by geolocation coordinates field, , all having a single geolocation
    dimension: ``profile`` (except ``z`` for Z axis coordinate).
      * ``lon(profile)``
      * ``lat(profile)``
      * ``time(profile)``
      * ``depth/alt (z)``
    """
    def get_geocoord_dimnames(
            self, fieldname: str, *args, **kwargs) -> Tuple[str, ...]:
        if fieldname in STANDARD_Z_FIELD or self.coords[fieldname].is_axis('Z'):
            return 'z',
        else:
            return 'profile',
