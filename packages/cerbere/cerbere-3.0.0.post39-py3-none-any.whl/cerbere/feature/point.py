# -*- coding: utf-8 -*-
"""
Feature class for a set of randomly sampled points.
"""
from __future__ import absolute_import, division, print_function

from cerbere.feature.feature import Feature

__all__ = ['Point']


class Point(Feature):
    """
    Feature class for a set of randomly sampled points.

    A :class:`~cerbere.feature.point.Point` feature is defined in CF convention
    by geolocation coordinates field: ``lon(obs)``, ``lat(obs)``,
    ``time(obs)``, optionally ``z(obs)``, all having a single geolocation
    dimension: ``obs``.
    """
    _instance_dimname = 'obs'
    _feature_geodimnames = ()

    def __init__(self, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)
        self._std_dataset.attrs['featureType'] = 'point'

    def get_geocoord_dimnames(self,  *args, **kwargs):
        return ()
