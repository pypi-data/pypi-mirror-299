"""
cerbere classes for common observation patterns.

.. autosummary::
    :toctree: _autosummary

    feature
    swath
    grid
    trajectory
"""
from cerbere.feature.cpoint import Point
from cerbere.feature.cprofile import Profile
from cerbere.feature.ctimeseries import TimeSeries
from cerbere.feature.ctrajectory import Trajectory
from cerbere.feature.ctimeseriesprofile import (TimeSeriesProfile,
                                                UniZTimeSeriesProfile)
from cerbere.feature.ctrajectoryprofile import TrajectoryProfile
from cerbere.feature.cimdcollection import IMDCollection
from cerbere.feature.comdcollection import OMDCollection
from cerbere.feature.cimage import Image
from cerbere.feature.cswath import Swath
from cerbere.feature.cgrid import Grid
from cerbere.feature.cgridtimeseries import GridTimeSeries
