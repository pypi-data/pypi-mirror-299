# -*- coding: utf-8 -*-
"""
Feature class for incomplete multidimensional collection of features.
"""
import typing as T

import xarray as xr

import cerbere
from cerbere.feature.cbasecollection import BaseCollection
from cerbere.feature.cbasefeature import BaseFeature

__all__ = ['IMDCollection']


class IMDCollection(BaseCollection):
    """
    Feature class for an incomplete multidimensional collection of features,
    as defined by Climate and Forecast convention:
    https://cfconventions.org/cf-conventions/cf-conventions.html
    #_incomplete_multidimensional_array_representation

    A :class:`~cerbere.feature.imdcollection.IMDCollection` class is defined by
    geolocation coordinates field and geolocation dimension of the feature, plus
    the instance dimension defined for this feature.

    For instance, for a :class:`~cerbere.feature.profile.Profile` feature, the
    instance dimension is ``profile``; the CF convention states that the
    geolocation coordinates field should be defined as: ``lon(profile)``,
    ``lat(profile)``, ``time(profile)``, ``z(profile, z)``; observation field
    should be defined as ``fieldname(profile, z)``.
    """

    @classmethod
    def from_list(
            cls,
            items: T.List[BaseFeature],
            feature_class: str = None) -> 'IMDCollection':
        """Build a collection feature from a list of features"""
        if feature_class is None:
            feature_class = items[0].__class__

        dst = xr.concat(
            [_.dataset for _ in items], dim=items[0]._instance_dimname
        ).rename_dims(
            {items[0]._instance_dimname: feature_class._instance_dimname})

        return IMDCollection(
            dst,
            feature_class=feature_class
        )

    @classmethod
    def guess_instance_var(cls, dataset: xr.Dataset):
        pass

    @classmethod
    def guess_instance_axis(cls, dataset: xr.Dataset):
        return dataset.cb.instance_dim

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset):

        for instance_class in ['Profile', 'Point']:
            try:
                cls._check_feature(dataset, instance_class=instance_class)
                return cls
            except cerbere.AxisError:
                pass

        # check if there is an instance variable
        instance_dims = dataset.cb.cf_instance_dims

        if len(instance_dims) == 0:
            return

        # to be a collection, the instance_var should have a dimension of
        # the same name
        for i_dim in instance_dims:
            if i_dim not in dataset.dims:
                return

        instance_dim = dataset.cb.cf_instance_dims[0]

        # verify conformity to IMD Collection
        # coordinates must be: X(i), Y(i), T(i), Z(i, z)
        inst_size = dataset.sizes[instance_dim]

        # lon(instance_dim,...)
        if not cls._check_coord_dims(dataset, 'lon', [instance_dim], inst_size):
            return
        # lat(instance_dim,...)
        if not cls._check_coord_dims(dataset, 'lat', [instance_dim], inst_size):
            return
        # time(instance_dim,...)
        if not cls._check_coord_dims(
                dataset, 'time', [instance_dim], inst_size):
            return

        # z(z)
        if dataset.cb.vertical is not None:
            z_size = dataset.cb.vertical.sizes
            if not len(z_size) == 2:
                return

        return cls
