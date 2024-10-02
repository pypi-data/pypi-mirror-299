# -*- coding: utf-8 -*-
"""
Feature class for a set of randomly sampled points.
"""
import typing as T

import xarray as xr

from cerbere.feature.cdiscretefeature import DiscreteFeature

__all__ = ['Point']


class Point(DiscreteFeature):
    """
    To represent data at scattered locations and times with no implied
    relationship among of coordinate positions, both data and coordinates
    must share the same (sample) instance dimension. Because each feature
    contains only a single data element, there is no need for a separate
    element dimension. The representation of point features is a special,
    degenerate case of the standard four representations. The coordinates
    attribute is used on the data variables to unambiguously identify the
    relevant space and time auxiliary coordinate variables.

    A :class:`~cerbere.feature.point.Point` feature is defined in CF convention
    by geolocation coordinates field: ``lon(obs)``, ``lat(obs)``,
    ``time(obs)``, optionally ``z(obs)``, all having a single geolocation
    dimension: ``obs``.
    """
    # must be defined for any feature corresponding to a CF discrete sampling
    # geometry, Nobe otherwise
    cf_feature_type = 'point'

    # the instance dimension name for collection of features
    cf_instance_axis = 'obs'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': (cf_instance_axis,),
        'latitude': (cf_instance_axis,),
        'time': (cf_instance_axis,),
        'vertical': (cf_instance_axis,),
        'data': (cf_instance_axis,)
    }

    # optional axes for the feature
    cf_optional_axes = ['vertical']

    # Unidata Common Data Model provides a wider set of feature types than CF
    cdm_data_type = 'point'

    def __init__(self, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[DiscreteFeature]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        # check lat/lon/time/z are zero dimensional
        for coord in ['longitude', 'latitude', 'time', 'vertical']:
            if not cls._check_coord_dims(dataset, coord,[]):
                return

        # check no axis coord
        if dataset.cb.cf_axis_coords != {}:
            return

        return Point
        #
        # if not (set(cfdst['lon'].dims) == set(cfdst['lat'].dims) == set(
        #         cfdst['time'].dims)):
        #     return
        # if cfdst.cb.Z is not None and set(cfdst['lon'].dims) != set(
        #         cfdst.cb.Z.dims):
        #     return
        # if len(set(cfdst['lon'].dims)) != 1 or cfdst['lon'].dims[0] == 'time':
        #     return
        #
        # # check provided axes if any
        # if cfdst.cb.X is not None and cfdst.cb.X.name != 'lon':
        #     return
        # if cfdst.cb.Y is not None and cfdst.cb.Y.name != 'lat':
        #     return
        # if cfdst.cb.T is not None and cfdst.cb.T.name != 'time':
        #     return
        #
        # return Point
