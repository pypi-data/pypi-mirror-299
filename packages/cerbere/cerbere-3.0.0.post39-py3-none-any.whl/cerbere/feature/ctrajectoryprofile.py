# -*- coding: utf-8 -*-
"""
Feature class for the trajectory of profile observation pattern.
"""
import typing as T
import warnings

import xarray as xr

import cerbere
from cerbere.feature.cbasecollection import BaseCollection
from cerbere.feature.comdcollection import OMDCollection
from cerbere.feature.cimdcollection import IMDCollection


__all__ = ['TrajectoryProfile']


class TrajectoryProfile(BaseCollection):
    """
    Feature class for the CF / Unidata CDM observation pattern corresponding to
    Profiles along a single trajectory.

    As defined in section H.6 of CF 1.11:
    "When profiles are taken along a trajectory, one gets a collection of
    profiles called a trajectoryProfile. A data variable may contain a
    collection of such trajectoryProfile features, one feature per
    trajectory. The instance dimension in the case of a trajectoryProfile is
    also referred to as the trajectory dimension. The instance variables,
    which have just this dimension, are also referred to as trajectory
    variables and are considered to contain information describing the
    trajectories. The trajectory variables may contain missing values. This
    allows one to reserve space for additional trajectories that may be added at
    a later time, as discussed in section 9.6. TrajectoryProfiles are more
    complicated than trajectories because there are two element dimensions.
    Each trajectory has a number of profiles as its elements, and each
    profile  has a number of data from various levels as its elements. It is
    strongly recommended that there always be a variable (of any data type) with
     the profile dimension and the cf_role attribute " profile_id ", whose
     values uniquely identify the profiles."

    More specifically, this class implements the case H.6.2. Profiles along a
    single trajectory:
    "If there is only one trajectory in the data variable, there is no need
    for the trajectory dimension"

    Case H.6.1. Multidimensional array representation of trajectory profiles
    is not yet implemented in this class.

    The variable(p,o) data for element o of profile p are associated with the
    coordinate values time(p), alt(p,o), lat(p), and lon(p). If all the
    profiles have the same set of vertical coordinates, the vertical
    auxiliary coordinate variable could be one-dimensional alt(z),
    or replaced by a one-dimensional coordinate variable  z(z), provided the
    values are ordered monotonically. In the latter case, listing the
    vertical coordinate variable in the coordinates attribute is optional.

    A :class:`~cerbere.feature.trajectory.Trajectory` feature is defined by
    geolocation coordinates field: ``lon(time)``, ``lat(time)``,
    ``time(time)``, optionally ``z(time)``, all having a single geolocation
    dimension: ``time``.
    """
    cf_instance_axis = 'trajectory'
    cf_element_instance_axis = 'profile'
    cf_feature_type = 'trajectoryProfile'
    cdm_data_type = 'trajectory_profile'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': (cf_instance_axis, 'profile'),
        'latitude': (cf_instance_axis, 'profile'),
        'time': (cf_instance_axis, 'profile'),
        'vertical': [(cf_instance_axis, 'profile', 'Z'),
                     (cf_instance_axis, 'Z')],
        'data': (cf_instance_axis, 'profile', 'Z')
    }
    # optional axes for the feature
    cf_optional_axes = []

    def __init__(self, *args, **kwargs):
        kwargs['instance_class'] = 'Profile'
        super().__init__(*args, **kwargs)

    @classmethod
    def cerberize(cls, dataset: xr.Dataset, force_reorder: bool = True,
                  **kwargs):
        cfdataset = super(TrajectoryProfile, cls).cerberize(
            dataset, force_reorder, **kwargs)

        # CF specific attrs and vars
        # It is strongly recommended that there always be a trajectory
        # variable (of any data type) with the attribute
        # cf_role=”trajectory_id” attribute, whose values uniquely identify
        # the trajectories.
        # if cfdataset.cb.cf_role is None:
        #     cfdataset['trajectory'] = xr.DataArray(
        #         dims=(),
        #         attrs={'cf_role': 'trajectory_id'},
        #         data=0)


        # for _, v in cfdataset.data_vars.items():
        #     v.encoding['coordinates'] = 'time lat lon z'

        return cfdataset

    @classmethod
    def _canonical_dims(cls, coord: str, instance_class=None) -> T.Set[str]:
        return instance_class.cf_canonical_dims[coord]

    @classmethod
    def is_alias(cls, dataset):
        # @TODO clarify if and which collection
        aliases = [
            _ for _ in [IMDCollection, OMDCollection]
            if _.guess_feature(dataset) is not None]
        if len(aliases) > 0:
            return aliases[0]

    @classmethod
    def guess_feature(
            cls, dataset: xr.Dataset
    ) -> T.Optional[T.Type['TrajectoryProfile']]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        try:
            cls._check_feature(dataset, instance_class='Profile')

            # to distinguish a TrajectoryProfile from a Collection of
            # profiles, there must be a variable with `cf_role` attribute
            # having value `trajectory_id`
            if 'trajectory_id' in dataset.cb.cf_role.values():
                return cls
        except cerbere.AxisError:
            return

