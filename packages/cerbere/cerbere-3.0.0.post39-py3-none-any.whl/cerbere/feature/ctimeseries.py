# -*- coding: utf-8 -*-
"""
Feature class for the time series observation pattern at a fix station.
"""
import typing as T
import xarray as xr
import warnings

from cerbere.dataset.dataset import STANDARD_Z_FIELD
from cerbere import CWarning
from cerbere.feature.cdiscretefeature import DiscreteFeature

__all__ = ['TimeSeries']


class TimeSeries(DiscreteFeature):
    """
    This class is for a single time series. This feature is defined by
    geolocation coordinates field: ``lon()``, ``lat()``, ``z()``,
    ``time(time)``,  none having a geolocation dimension (except ``time`` for T
    axis coordinate).

    Refer to CF convention: https://cfconventions.org/cf-conventions/cf
    -conventions.html#time-series

    Data may be taken over periods of time at a set of discrete point,
    spatial locations called stations (see also discussion in 9.1).  The set
    of elements at a particular station is referred to as a timeSeries
    feature and a data variable may contain a collection of such features.
    The instance dimension in the case of timeSeries specifies the number of
    time series in the collection and is also referred to as the station
    dimension. The instance variables, which have just this dimension,
    including latitude and longitude for example, are also referred to as
    station variables and are considered to contain information describing
    the stations. The station variables may contain missing values, allowing
    one to reserve space for additional stations that may be added at a later
    time, as discussed in section 9.6. In addition,
    * It is strongly recommended that there should be a station variable (
      which may be of any type) with the attribute cf_role=”timeseries_id”,
      whose values uniquely identify the stations.
    * It is recommended that there should be station variables with
      standard_name attributes " platform_name ", " surface_altitude " and “
      platform_id ” when applicable.

    All the representations described in section 9.3 can be used for time
    series. The global attribute featureType=”timeSeries” (case-insensitive)
    must be included.
    """
    cf_instance_axis = 'station'
    cf_feature_type = 'timeSeries'
    cdm_data_type = 'station'

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'latitude': (cf_instance_axis,),
        'longitude': (cf_instance_axis,),
        'time': (cf_instance_axis, 'T'),
        'vertical': (cf_instance_axis,),
        'data': (cf_instance_axis, 'T')
    }
    # optional axes for the feature
    cf_optional_axes = ['vertical']

    @classmethod
    def cerberize(cls, dataset: xr.Dataset, force_reorder: bool = True,
                  **kwargs):
        cfdataset = super(TimeSeries, cls).cerberize(dataset, force_reorder)

        # CF specific attrs and vars
        # It is strongly recommended that there should be a station variable
        # (which may be of any type) with the attribute
        # cf_role=”timeseries_id”, whose values uniquely identify the stations.
        # It is recommended that there should be station variables with
        # standard_name attributes " platform_name ", " surface_altitude "
        # and “ platform_id ” when applicable.
        if cfdataset.cb.cf_role is None:
            station_var = None
            for varname in cfdataset.variables:
                v = cfdataset.variables[varname]
                if v.attrs.get('standard_name') == 'platform_name' or \
                        v.attrs.get('standard_name') == 'platform_id':
                    cfdataset[v].cf_role = 'timeseries_id'
                    station_var = v
                    break

            if station_var is None:
                cfdataset['station_id'] = xr.DataArray(
                    dims=(),
                    attrs={'cf_role': 'timeseries_id'},
                    data=0
                )

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

        # check lat/lon are axes and single value
        for coordname in ['lon', 'lat']:
            if len(cfdst[coordname].dims) != 0 or cfdst[coordname].size != 1:
                return
        if set(cfdst['lon'].dims) != set(cfdst['lat'].dims):
            return

        # check time has only one axis which is time
        if len(cfdst['time'].dims) != 1 or 'time' not in cfdst['time'].dims:
            return

        # check provided axes if any
        if cfdst.cb.X is not None and cfdst.cb.X.name != 'lon':
            return
        if cfdst.cb.Y is not None and cfdst.cb.Y.name != 'lat':
            return
        if cfdst.cb.T is not None and cfdst.cb.T.name != 'time':
            return

        return TimeSeries
