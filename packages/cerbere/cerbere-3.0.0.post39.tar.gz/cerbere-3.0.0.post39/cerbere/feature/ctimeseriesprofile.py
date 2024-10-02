# -*- coding: utf-8 -*-
"""
Feature class for the time series of profiles observation pattern.
"""
import typing as T

import xarray as xr

import cerbere
from cerbere.feature.cbasecollection import BaseCollection
from cerbere.feature.cimdcollection import IMDCollection
from cerbere.feature.comdcollection import OMDCollection


class TimeSeriesProfile(BaseCollection):
    """
    This class is for a single time series. This feature is defined by
    geolocation coordinates field: ``lon()``, ``lat()``, ``z()``,
    ``time(time)``,  none having a geolocation dimension (except ``time`` for T
    axis coordinate).

    Refer to CF convention: https://cfconventions.org/cf-conventions/cf
    -conventions.html#time-series-ptofiles

    When profiles are taken repeatedly at a station, one gets a time series
    of profiles (see also section H.2 for discussion of stations and time
    series). The resulting collection of profiles is called a
    timeSeriesProfile. A data variable may contain a collection of such
    timeSeriesProfile features, one feature per station. The instance
    dimension in the case of a timeSeriesProfile is also referred to as the
    station dimension. The instance variables, which have just this
    dimension, including latitude and longitude for example, are also
    referred to as station variables and are considered to contain
    information describing the stations. The station variables may contain
    missing values. This allows one to reserve space for additional stations
    that may be added at a later time, as discussed in section 9.6. In addition,

    * It is strongly recommended that there should be a station variable (
      which may be of any type) with cf_role attribute "timeseries_id",
      whose values uniquely identify the stations.
    * It is recommended that there should be station variables with
      standard_name attributes "platform_name", "surface_altitude" and
     “platform_id” when applicable.

    TimeSeriesProfiles are more complicated than timeSeries because there are
    two element dimensions (profile and vertical). Each time series has a
    number of profiles from different times as its elements, and each profile
    has a number of data from various levels as its elements. It is strongly
    recommended that there always be a variable (of any data type) with the
    profile dimension and the cf_role attribute " profile_id ", whose values
    uniquely identify the profiles.

    A :class:`~cerbere.feature.timeseriesprofile.TimeSeriesProfile` feature is
    defined by geolocation coordinates field, , all having a single geolocation
    dimension: ``profile`` (except ``z`` for Z axis coordinate).
      * ``lon(profile)``
      * ``lat(profile)``
      * ``time(profile)``
      * ``depth/alt (profile, z)``
    """
    cf_instance_axis = 'station'
    cf_element_instance_axis = 'profile'
    cf_instance_role = 'timeseries_id'
    cf_feature_type = 'timeSeriesProfile'
    cdm_data_type = 'station_profile'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'longitude': (cf_instance_axis,),
        'latitude': (cf_instance_axis,),
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

        # self.cf_role_var = self.cf_role()

        # CF specific attrs and vars for profile feature
        self.ds.attrs['featureType'] = 'timeSeriesProfile'

    @classmethod
    def is_alias(cls, dataset):
        # @TODO clarify if and which collection
        aliases = [
            _ for _ in [IMDCollection, OMDCollection]
            if _.guess_feature(dataset) is not None]
        if len(aliases) > 0:
            return aliases[0]

    # @classmethod
    # def _canonical_dims(cls, coord: str, instance_class=None) -> T.Set[str]:
    #     return set(cls.cf_canonical_dims[coord]) - {cls.cf_instance_axis}

    @classmethod
    def _canonical_dims(cls, coord: str, instance_class=None) -> T.Set[str]:
        if coord in ['latitude', 'longitude', 'time']:
            return set(cls.cf_canonical_dims[coord]) - {cls.cf_instance_axis}

        return instance_class.cf_canonical_dims[coord]

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[IMDCollection]:

        cfdst = dataset.cb.cfdataset

        # @TODO: check role attributes

        # check CF featureType and Unidata CDM' feature type are compatible
        # with this feature
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        try:
            cls._check_feature(dataset, instance_class='Profile')
            return cls
        except cerbere.AxisError:
            pass


class UniZTimeSeriesProfile(OMDCollection):
    """
    Feature class for the time series of profiles observation pattern, where z
    is unique and identical for each profile in the series.

    A :class:`~cerbere.feature.timeseriesprofile.TimeSeriesProfile` feature is
    defined by geolocation coordinates field, all having a single geolocation
    dimension: ``profile`` (except ``z`` for Z axis coordinate).
      * ``lon(profile)``
      * ``lat(profile)``
      * ``time(profile)``
      * ``depth/alt (z)``
    """
    cf_instance_axis = 'timeseries_id'
    cf_feature_type = 'timeSeriesProfile'
    cdm_data_type = 'timeseries_profile'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'X': (cf_instance_axis,),
        'Y': (cf_instance_axis,),
        'T': (cf_instance_axis, 'profile'),
        'Z': (cf_instance_axis, 'Z'),
        'data': (cf_instance_axis, 'profile', 'Z')
    }

    def __init__(self, *args, **kwargs):
        kwargs['instance_class'] = 'Profile'
        super().__init__(*args, **kwargs)

        #self.cf_role_var = self.ds.cf_role()

        # CF specific attrs and vars for profile feature
        self.ds.attrs['featureType'] = 'timeSeriesProfile'

    @classmethod
    def is_alias(cls):
        return OMDCollection

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional[IMDCollection]:

        cfdst = dataset.cb.cfdataset

        # check CF featureType and Unidata CDM' feature type
        if cls._unexpected_featureType(cfdst) or \
                cls._unexpected_cdm_data_type(cfdst):
            return

        # check lat/lon/time are axes with a single dimension which profile
        for coordname in ['lon', 'lat', 'time']:
            if len(cfdst[coordname].dims) != 0:
                return

        # check provided axes if any
        if cfdst.cb.Z is not None:
            if len(cfdst[cfdst.cb.Z.name].dims) != 2 and \
                    cfdst[cfdst.cb.Z.name].dims[0] != 'profile':
                return

        return cls