#!/usr/bin/env python
# coding=utf-8
"""
"""
import datetime
from .exceptions import *
from .helpers import *

import numpy as np

# import features
from cerbere.feature.cbasefeature import BaseFeature
from cerbere.feature.cgrid import Grid
from cerbere.feature.cimdcollection import IMDCollection
from cerbere.feature.comdcollection import OMDCollection
from cerbere.feature.cpoint import Point
from cerbere.feature.cprofile import Profile
from cerbere.feature.cracollection import CRACollection
from cerbere.feature.cswath import Swath
from cerbere.feature.ctimeseries import TimeSeries
from cerbere.feature.ctimeseriesprofile import TimeSeriesProfile
from cerbere.feature.ctrajectory import Trajectory
from cerbere.feature.ctrajectoryprofile import TrajectoryProfile


# preserve the variable attributes during xarray operations
xr.set_options(keep_attrs=True)


def dt64todatetime(dt64):
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    seconds_since_epoch = (dt64 - unix_epoch) / one_second

    if isinstance(seconds_since_epoch, xr.DataArray):
        seconds_since_epoch = seconds_since_epoch.data.item()

    return datetime.datetime.utcfromtimestamp(seconds_since_epoch)
