# -*- coding: utf-8 -*-
"""
Feature class for the trajectory observation pattern.
"""
import typing as T

import xarray as xr

import cerbere
from cerbere.feature.cdiscretefeature import DiscreteFeature


__all__ = ['Trajectory']


class Trajectory(DiscreteFeature):
    """
    Feature class for the trajectory observation patterns.

    A :class:`~cerbere.feature.trajectory.Trajectory` feature is defined by
    geolocation coordinates field: ``lon(time)``, ``lat(time)``,
    ``time(time)``, optionally ``z(time)``, all having a single geolocation
    dimension: ``time``.
    """
    cf_instance_axis = 'trajectory'
    cf_feature_type = 'trajectory'
    cdm_data_type = 'trajectory'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'latitude': (cf_instance_axis, 'T'),
        'longitude': (cf_instance_axis, 'T'),
        'time': (cf_instance_axis, 'T'),
        'vertical': [(cf_instance_axis, 'T'), (cf_instance_axis,)],
        'data': (cf_instance_axis, 'T')
    }
    # optional axes for the feature
    cf_optional_axes = ['vertical']

    @classmethod
    def cerberize(cls, dataset: xr.Dataset, force_reorder: bool = True,
                  **kwargs):
        cfdataset = super(Trajectory, cls).cerberize(dataset, force_reorder)

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
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[DiscreteFeature]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        try:
            cls._check_feature(dataset)
            return cls
        except cerbere.AxisError:
            pass

        # # check lat/lon/time are axes with a single time dimension
        # for axis in ['X', 'Y', 'T', 'Z']:
        #     if axis == 'Z' and axis not in dataset.cb.cf_axis_coords and \
        #             cfdst.cb.vertical is None:
        #         continue
        #     if not cls._check_coord_dims(
        #             dataset,
        #             dataset.cb.cf_axis_coords[axis],
        #             [dataset.cb.cf_axis_dims['T']]):
        #         return
        #
        # # check provided axes if any
        # # if cfdst.cb.X is not None and cfdst.cb.X.name != 'lon':
        # #     return
        # # if cfdst.cb.Y is not None and cfdst.cb.Y.name != 'lat':
        # #     return
        # # if cfdst.cb.T is not None and cfdst.cb.T.name != 'time':
        # #     return
        #
        # return Trajectory
