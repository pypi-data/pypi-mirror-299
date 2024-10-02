# -*- coding: utf-8 -*-
"""
Feature class for contiguous ragged array collection of features, as defined
by CF convention.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

import xarray as xr

from cerbere.feature.feature import Feature


class CRACollection(Feature):
    """
    Feature class for a contiguous ragged array collection of features.

    A :class:`~cerbere.feature.cracollection.CRACollection` class is defined by
    geolocation coordinates field and geolocation dimension of the feature, plus
    the instance dimension defined for this feature.

    For instance, for a :class:`~cerbere.feature.trajectory.Trajectory` feature,
    the instance dimension is ``profile``; the CF convention states that the
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
        if feature_class.__name__ not in ['Trajectory', 'Profile']:
            raise ValueError(
                'A CRACollection can not contain this type of feature'
            )
        self.feature_class = feature_class
        super(CRACollection, self).__init__(*args, **kwargs)

        self._std_dataset.attrs['featureType'] = feature_class._instance_dimname

    @property
    def _feature_geodimnames(self):
        return (self.feature_class._instance_dimname,) + \
               self.feature_class._feature_geodimnames

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height']:
            return 'z',
        else:
            return self.feature_class._instance_dimname

    # @classmethod
    # def from_list(cls, features):
    #     """Build the collection object from a list of features"""
    #     rowsize = []
    #
    #     for feature in features:
    #         # trajectory => T
    #         # profile => Z
    #         rowsize.append(
    #             feature.sizes[feature._get_collection_axis()])
    #         for v in feature.variables:
