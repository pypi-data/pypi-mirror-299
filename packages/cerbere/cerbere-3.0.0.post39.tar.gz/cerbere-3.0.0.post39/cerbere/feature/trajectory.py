# -*- coding: utf-8 -*-
"""
Feature class for the trajectory observation pattern.
"""
from __future__ import absolute_import, division, print_function

from cerbere.feature.feature import Feature

__all__ = ['Trajectory']


class Trajectory(Feature):
    """
    Feature class for the trajectory observation patterns.

    A :class:`~cerbere.feature.trajectory.Trajectory` feature is defined by
    geolocation coordinates field: ``lon(time)``, ``lat(time)``,
    ``time(time)``, optionally ``z(time)``, all having a single geolocation
    dimension: ``time``.
    """
    _instance_dimname = 'trajectory'
    _feature_geodimnames = 'time',

    def get_geocoord_dimnames(self,  *args, **kwargs):
        return 'time',
