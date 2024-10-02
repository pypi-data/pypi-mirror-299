# -*- coding: utf-8 -*-
"""
Feature class for the time series observation pattern at a fix station.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

from cerbere.dataset.dataset import STANDARD_Z_FIELD
from cerbere.feature.feature import Feature

__all__ = ['TimeSeries']


class TimeSeries(Feature):
    """
    Feature class for the time series observation patterns.

    A :class:`~cerbere.feature.timeseries.TimeSeries` feature is defined by
    geolocation coordinates field: ``lon()``, ``lat()``,
    ``time(time)``, ``depth/alt ()``, none having a geolocation dimension
    (except ``time`` for T axis coordinate).
    """
    _instance_dimname = 'station'
    _feature_geodimnames = 'time',

    def __init__(self, *args, **kwargs):
        super(TimeSeries, self).__init__(*args, **kwargs)

        # CF specific attrs and vars for profile feature
        self._std_dataset.attrs['featureType'] = 'timeSeries'

        # mandatory coordinates
        for _, v in self._std_dataset.data_vars.items():
            v.attrs['coordinates'] = 'time lat lon z'

    def get_geocoord_dimnames(
            self, fieldname: str, *args, **kwargs) -> Tuple[str, ...]:
        if (fieldname in STANDARD_Z_FIELD + ['lat', 'lon'] or
                self.coords[fieldname].is_axis('Z')):
            return ()
        else:
            return 'time',
