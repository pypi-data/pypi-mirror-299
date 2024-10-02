# -*- coding: utf-8 -*-
"""
Base class for a collection of features.
"""
import typing as T

import cerbere
from cerbere.feature.cbasefeature import BaseFeature
from cerbere.feature.cdiscretefeature import DiscreteFeature


class BaseCollection(DiscreteFeature):
    """
    Feature class for collection of features.
    """
    def __init__(
            self,
            dataset,
            instance_class: str = None,
            **kwargs):
        """
        Args:
            feature_class (BaseFeature) : the feature class which the
                collection is made of.

        See:
            BaseFeature
        """
        if instance_class is None:
            # try to infer from dataset
            instance_class = BaseCollection.infer_instance_class(dataset)
            if instance_class is None:
                raise ValueError(
                    'A value must be provided for ``feature_class`` arg'
                )
        self.instance_class = cerbere.feature_class(instance_class)

        self.cf_canonical_dims = self.instance_class.cf_canonical_dims
        if self.cf_instance_axis is None:
            self.cf_instance_axis = self.instance_class.cf_instance_axis

        super().__init__(dataset, instance_class=instance_class, **kwargs)

        if self.dataset.attrs.get('featureType') is not None:
            return

        if self.cf_feature_type is None:
            self.dataset.attrs['featureType'] =  (
                self.instance_class.cf_feature_type)
        else:
            self.dataset.attrs['featureType'] = self.cf_feature_type


    @staticmethod
    def infer_instance_class(dataset):
        if dataset.cb.featureType is not None:
            for feature in cerbere.helpers._feature:
                feat_class = cerbere.feature_class(feature)
                if not issubclass(feat_class, DiscreteFeature):
                    continue
                if dataset.cb.featureType == feat_class.cf_feature_type:
                    return feature

        # try to fit one of the features
        if len(dataset.cb.cf_instance_dims) > 0:
            item = dataset.cb.isel({dataset.cb.cf_instance_dims[0]: 0})
            for feature in ['Profile', 'Point']:
                feat_class = cerbere.feature_class(feature)
                if issubclass(feat_class, DiscreteFeature):
                    try:
                        #cerbere.guess_feature(item)
                        feat_class._check_feature(item)
                        return feature
                    except (cerbere.AxisError, TypeError):
                        pass

    @classmethod
    def _canonical_dims(cls, coord: str, instance_class=None) -> T.Set[str]:
        if isinstance(instance_class.cf_canonical_dims[coord], list):
            return instance_class.cf_canonical_dims[coord][0]
        return instance_class.cf_canonical_dims[coord]

    @classmethod
    def required_dims(cls, instance_class):
        return (instance_class.cf_instance_axis,
                ) + instance_class.cf_canonical_dims

    def __getitem__(self, item):
        """For iterating over the features of a collection"""
        instance_axis = self.ds.cb.cf_instance_dims[0]

        if isinstance(item, int):
            if item >= self.dataset.sizes[instance_axis]:
                raise IndexError("index out of range")

            return self.instance_class(self.dataset.isel({instance_axis: item}))
        else:
            return self.__class__(
                self.dataset.isel({instance_axis: item}))

    def __len__(self):
        instance_axis = self.instance_class.cf_instance_axis

        return self.dataset.dims[instance_axis]
