# -*- coding: utf-8 -*-
"""
Feature class for the profile observation pattern.
"""
import logging
import typing as T

import numpy as np
import xarray as xr

from cerbere.feature.cdiscretefeature import DiscreteFeature


__all__ = ['Profile']


class Profile(DiscreteFeature):
    """
    Feature class for the profile observation patterns.

    A :class:`~cerbere.feature.profile.Profile` feature is defined by
    coordinates:
    * ``lon()`` or ``lon(profile)``
    * ``lat()`` or ``lat(profile)``
    * ``time()`` or ``time(profile)``
    * ``z(z)``
    * ``profile()`` of any type

    """
    # must be defined for any feature corresponding to a CF discrete sampling
    # geometry, Nobe otherwise
    cf_feature_type = 'profile'

    # the instance dimension name for collection of features
    cf_instance_axis = 'profile'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    # x, y, z, t refer to the coordinates; X, Y, Z, T to the dimensions
    cf_canonical_dims = {
        'longitude': (cf_instance_axis,),
        'latitude': (cf_instance_axis,),
        'time': (cf_instance_axis,),
        'vertical': [(cf_instance_axis, 'Z'), ('Z',)],
        'data': (cf_instance_axis, 'Z')
    }
    # optional axes for the feature
    cf_optional_axes = []

    # Unidata Common Data Model provides a wider set of feature types than CF
    cdm_data_type = 'profile'

    @classmethod
    def cerberize(cls, dataset: xr.Dataset, force_reorder: bool = True,
                  **kwargs):
        """modify a dataset so that it fully fits the feature's data model"""
        cfdataset = super(Profile, cls).cerberize(dataset, force_reorder)

        # CF specific attrs and vars for profile feature
        if 'profile' not in cfdataset and cfdataset.cb.cf_role is None:
            logging.debug('adding a dummy profile variable as none was '
                          'provided')
            cfdataset['profile'] = xr.DataArray(
                dims=(),
                attrs={'cf_role': 'profile_id'},
                data=np.empty((), dtype=np.int)
            )

        for _, v in cfdataset.data_vars.items():
            v.encoding['coordinates'] = 'time lat lon z'

        return cfdataset

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[DiscreteFeature]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        if len(dataset.cb.cf_instance_dims) != 0:
            return

        # if dataset.cb.instance_dim is not None:
        #     profile = dataset.cf.instance_dim
        #     if not (
        #         cls._check_coord_dims(dataset, 'latitude', profile, 1) and
        #         cls._check_coord_dims(dataset, 'latitude', profile, 1) and
        #         cls._check_coord_dims(dataset, 'time', profile, 1) and
        #         cls._check_coord_dims(dataset, dataset.cb.vertical,
        #                               dataset.cb.cf_axis_dims['Z'], None)
        #     ):
        #         return

        for coord in ['longitude', 'latitude', 'time']:
            if not cls._check_coord_dims(dataset, coord, []):
                return
        if not cls._check_coord_dims(
                dataset, 'vertical', dataset.cb.cf_axis_dims['Z'],None):
            return

        return Profile
