# -*- coding: utf-8 -*-
"""
Feature class for orthogonal multidimensional collection of features.
"""
import typing as T

import xarray as xr

import cerbere
from cerbere.feature.cbasecollection import BaseCollection
from cerbere.feature.cbasefeature import BaseFeature


__all__ = ['OMDCollection']


class OMDCollection(BaseCollection):
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
    @classmethod
    def from_list(
            cls,
            items: T.List[BaseFeature],
            feature_class: BaseFeature = None) -> 'OMDCollection':
        """Build a collection feature from a list of feature instances"""
        if feature_class is None:
            feature_class = items[0].__class__

        dst = xr.concat(
            [_.dataset for _ in items], dim=items[0]._instance_dimname
        ).rename_dims(
            {items[0]._instance_dimname: feature_class._instance_dimname})

        return OMDCollection(
            dst,
            feature_class=feature_class
        )

    @classmethod
    def _canonical_dims(
            cls, coord: str, instance_class=None
    ) -> T.Union[T.List[T.Set[str]], T.Set[str]]:
        if coord == 'vertical':
            if isinstance(instance_class.cf_canonical_dims[coord], list):
                return [set(_) - {instance_class.cf_instance_axis}
                        for _ in instance_class.cf_canonical_dims[coord]]
            else:
                return set(instance_class.cf_canonical_dims[coord]) - \
                    {instance_class.cf_instance_axis}
        else:
            return set(instance_class.cf_canonical_dims[coord])

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset):

        for instance_class in ['Profile', 'Point']:
            try:
                cls._check_feature(dataset, instance_class=instance_class)
                print(instance_class)
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

        # verify conformity to OMD Collection
        # coordinates must be: X(i), Y(i), T(i), Z(z)
        inst_size = dataset.sizes[instance_dim]

        # lon(instance_dim,...)
        check_lon = cls._check_coord_dims(
            dataset, 'lon', [instance_dim], inst_size)
        # lat(instance_dim,...)
        check_lat = cls._check_coord_dims(
            dataset, 'lat', [instance_dim], inst_size)
        # time(instance_dim,...)
        check_time = cls._check_coord_dims(
            dataset, 'time', [instance_dim], inst_size)

        check_z = True
        # two cases
        # z(z)
        # z() : degenerate case with no Z axis
        if dataset.cb.vertical is not None and 'Z' in dataset.cb.cf_axis_dims:
            z_size = dataset.cb.vertical.sizes

            # z(z)
            check_z = len(z_size) == 1 and cls._check_coord_dims(
                dataset, dataset.cb.vertical.name,
                [dataset.cb.vertical.name],
                list(z_size.values())[0])

        if all([check_lon, check_lat, check_time, check_z]):
            return cls

