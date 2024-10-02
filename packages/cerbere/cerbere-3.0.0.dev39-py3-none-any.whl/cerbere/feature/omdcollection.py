# -*- coding: utf-8 -*-
"""
Feature class for orthogonal multidimensional collection of features.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

import xarray as xr

from cerbere.feature.feature import Feature

__all__ = ['OMDCollection']


class OMDCollection(Feature):
    """
    Feature class for an orthogonal multidimensional collection of features.

    A :class:`~cerbere.feature.omdcollection.OMDCollection` class is defined by
    geolocation coordinates field and geolocation dimension of the feature, plus
    the instance dimension defined for this feature.

    For instance, for a :class:`~cerbere.feature.profile.Profile` feature, the
    instance dimension is ``profile``; the CF convention states that the
    geolocation coordinates field should be defined as: ``lon(profile)``,
    ``lat(profile)``, ``time(profile)``, ``z(z)``; observation field should be
    defined as ``fieldname(profile, z)``.
    """
    def __init__(
            self,
            *args,
            feature_class: 'Feature' = None,
            **kwargs):
        """
        Args:
            feature_class (Feature) : the feature class which the collection is
                made of.

        See:
        Feature
        """
        if feature_class is None:
            raise ValueError(
                'A value must be provided for ``feature_class`` arg'
            )
        self.feature_class = feature_class
        super(OMDCollection, self).__init__(*args, **kwargs)

        self._std_dataset.attrs['featureType'] = feature_class._instance_dimname

    @property
    def _feature_geodimnames(self):
        return (self.feature_class._instance_dimname,) + \
               self.feature_class._feature_geodimnames

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height']:
            return self.feature_class._feature_geodimnames
        else:
            return self.feature_class._instance_dimname
