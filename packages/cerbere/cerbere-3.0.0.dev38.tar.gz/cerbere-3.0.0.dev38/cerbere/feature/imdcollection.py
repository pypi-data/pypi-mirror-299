# -*- coding: utf-8 -*-
"""
Feature class for incomplete multidimensional collection of features.
"""
from __future__ import absolute_import, division, print_function

from typing import List, Tuple

import xarray as xr

from cerbere.feature.feature import Feature

__all__ = ['IMDCollection']


class IMDCollection(Feature):
    """
    Feature class for an incomplete multidimensional collection of features.

    A :class:`~cerbere.feature.imdcollection.IMDCollection` class is defined by
    geolocation coordinates field and geolocation dimension of the feature, plus
    the instance dimension defined for this feature.

    For instance, for a :class:`~cerbere.feature.profile.Profile` feature, the
    instance dimension is ``profile``; the CF convention states that the
    geolocation coordinates field should be defined as: ``lon(profile)``,
    ``lat(profile)``, ``time(profile)``, ``z(profile, z)``; observation field
    should be defined as ``fieldname(profile, z)``.
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
        super(IMDCollection, self).__init__(*args, **kwargs)

        self._std_dataset.attrs['featureType'] = feature_class._instance_dimname

    @property
    def _feature_geodimnames(self):
        return (self.feature_class._instance_dimname,) + \
               self.feature_class._feature_geodimnames

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height']:
            return ((self.feature_class._instance_dimname,) +
                    self.feature_class._feature_geodimnames)
        else:
            return self.feature_class._instance_dimname

    @classmethod
    def from_list(
            cls,
            items: List['Feature'],
            feature_class: 'Feature' = None) -> 'IMDCollection':
        """Build a collection feature from a list of features"""
        if feature_class is None:
            feature_class = items[0].__class__

        dst = xr.concat(
            [_.to_xarray() for _ in items], dim=items[0]._instance_dimname
        ).rename_dims(
            {items[0]._instance_dimname: feature_class._instance_dimname})

        return IMDCollection(
            dst,
            feature_class=feature_class
        )


