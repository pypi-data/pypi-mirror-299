# encoding: utf-8
"""
Abstract class for discrete data feature objects
"""
import typing as T

import xarray as xr

from .cbasefeature import BaseFeature


class DiscreteFeature(BaseFeature):

    # Each type of discrete sampling geometry (point, time series, profile or
    # trajectory) is defined by the relationships among its spatiotemporal
    # coordinates. We refer to the type of discrete sampling geometry as its
    # featureType. The term “ feature ” refers herein to a single instance of
    # the discrete sampling geometry (such as a single time series).
    # the following class attributes define the expected dimensions and shape
    # of the CF features

    # must be defined for any feature corresponding to a CF discrete sampling
    # geometry, Nobe otherwise
    cf_feature_type = None

    # the instance dimension name for collection of features
    cf_instance_axis = None

    # the instance dimension name for collection of features which are
    # themselves collections (like TimeSeriesProfile, TrajectoryProfile,...)
    cf_element_instance_axis = None

    @classmethod
    def _unexpected_featureType(cls, cfdst):
        """check CF featureType"""
        if cls.cf_feature_type is None or cfdst.cb.featureType is None:
            return False
        return cfdst.cb.featureType.lower() != cls.cf_feature_type.lower()

    @classmethod
    def _canonical_dims(
            cls, coord: str, *args, **kwargs
    ) -> T.Union[T.Set[str], T.List[T.Set[str]]]:
        if isinstance(cls.cf_canonical_dims[coord], list):
            return [set(_) - {cls.cf_instance_axis}
                    for _ in cls.cf_canonical_dims[coord]]
        return set(cls.cf_canonical_dims[coord]) - {cls.cf_instance_axis}

    @classmethod
    def cerberize(
            cls,
            dataset: xr.Dataset,
            force_reorder: bool = True,
            instance_class: 'BaseFeature' = None
    ) -> xr.Dataset:

        ds = super().cerberize(
            dataset, force_reorder=force_reorder, instance_class=instance_class)

        # fill in feature type attributes
        if cls.cf_feature_type is not None:
            ds.attrs['featureType'] = cls.cf_feature_type

        return ds
