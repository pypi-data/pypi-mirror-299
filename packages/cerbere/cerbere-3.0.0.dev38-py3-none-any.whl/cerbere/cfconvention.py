# -*- coding: utf-8 -*-
"""
Definition of Cerbere Climate & Forecast convention profile
"""
import collections
from enum import Enum
import inspect
import logging
import os
from typing import Any, Mapping

import yaml

import numpy as np


CF_AUTHORITY = 'CF-1.11, ACDD-1.3'

# Module level default values
DEFAULT_TIME_UNITS = 'seconds since 1981-01-01 00:00:00'

# format for printing times
FORMAT_TIME = '%Y-%m-%dT%H:%M:%SZ'

# standard CF structuring dimensions
CF_DIMS = [u'time', u'lat', u'lon', u'z', u'obs', u'profile', u'row', u'cell']

# Standard CF Axis attribute values
CF_AXIS = ['X', 'Y', 'Z', 'T']

# Standard CF coordinates
CF_COORDS = ['latitude', 'longitude', 'vertical', 'time']

# Cerbere naming for CF coordinate
CB_COORD_CONVENTION = {'latitude': 'lat', 'longitude': 'lon', 'time': 'time'}

CF_COORD_AXIS = {
    'latitude': 'Y',
    'longitude': 'X',
    'time': 'T',
    'vertical': 'Z'}

# Standard CF coordinate units
CF_COORD_UNITS = {
    'lat': ['degrees_north', 'degree_north', 'degree_N', 'degrees_N',
            'degreeN', 'degreesN'],
    'lon': ['degrees_east', 'degree_east', 'degree_E', 'degrees_E', 'degreeE',
            'degreesE'],
}

# standard geolocation coordinates
CF_REQ_GEOCOORDS = ['time', 'latitude', 'longitude']
GEOCOORDS = CF_REQ_GEOCOORDS + ['vertical']

GEOCOORD_AXIS = {
    'latitude': 'Y', 'longitude': 'X', 'time': 'T', 'vertical': 'Z'}

# standard attributes for geolocation coordinates
GEOCOORD_ATTRS = {
    'latitude': {
        'standard_name': 'latitude', 'units': 'degree_north',
        'long_name': 'latitude', 'authority': CF_AUTHORITY},
    'longitude': {
        'standard_name': 'longitude', 'units': 'degree_east',
        'long_name': 'longitude', 'authority': CF_AUTHORITY},
    'time': {
        'standard_name': 'time', 'long_name': 'time',
        'authority': CF_AUTHORITY},
}

# CF standard names for geolocation coordinates
GEOCOORD_STD_NAME = {
    'latitude': ['latitude'],
    'longitude': ['longitude'],
    'time': ['time'],
    # remove any value in 'vertical' as it is too ambiguous with non
    # coodinate variables
    'vertical': [],
}

# coverage_content_type (ACDD 1.3): an ISO 19115-1 code to indicate the
# source of the data.
COVERAGE_CONTENT_TYPE = [
    'image', 'thematicClassification', 'physicalMeasurement',
    'auxiliaryInformation', 'qualityInformation', 'referenceInformation',
    'modelResult', 'coordinate'
]

CDM2CF_FEATURE = {
    'grid': None,
    'swath': None,
    'curvilinear': None,
    'point': 'point',
    'profile': 'profile',
    'station': 'timeSeries',
    'trajectory': 'trajectory',
    'station_profile': 'timeSeriesProfile',
    'trajectory_profile': 'trajectoryProfile'
}

"""
public enum ucar.nc2.constants.FeatureType {
  ANY,        // No specific type

  COVERAGE,   // any of the coverage types: GRID, FMRC, SWATH, CURVILINEAR
  GRID,       // seperable coordinates
  FMRC,       // two time dimensions, runtime and forecast time
  SWATH,      // 2D latlon, dependent time, polar orbiting satellites
  CURVILINEAR,// 2D latlon, independent time

  ANY_POINT,  // Any of the point types
  POINT,      // unconnected points
  PROFILE,    // fixed x,y with data along z
  STATION,    // timeseries at named location
  STATION_PROFILE, // timeseries of profiles
  TRAJECTORY, // connected points in space and time
  TRAJECTORY_PROFILE, //  trajectory of profiles

  RADIAL,     // polar coordinates
  STATION_RADIAL, // time series of radial data

  // experimental
  IMAGE,    // pixels, may not be geolocatable
  UGRID;    // unstructured grids
}
"""


def default_fill_value(obj):
    """Returns the default fill value for a specific type"""
    if isinstance(obj, np.dtype):
        dtype = obj
    elif isinstance(obj, (str, type)):
        dtype = np.dtype(obj)
    elif isinstance(obj, np.ndarray):
        dtype = obj.dtype
    else:
        raise TypeError('Unexpected object type: ', type(obj), obj)

    if np.issubdtype(dtype, np.datetime64):
        return np.datetime64('NaT')

    if np.issubdtype(dtype, np.integer):
        # return the maximum for numbers, the minimum for relative numbers
        info = np.iinfo(dtype)
        if info.min == 0:
            return dtype.type(info.max)
        return dtype.type(info.min)

    return dtype.type(np.ma.default_fill_value(dtype))


def default_profile(
        profile: str='default_saving_profile.yaml') -> Mapping[str, Any]:
    """Returns a list of default settings for storing data and metadata

    The settings are defined in a YAML file and can include a liste of global
    attributes (and default values), variable attributes (and default values)
    and variable encoding (scale_factor, add_offset,...) for a given storage
    format. If no profile file is provided, the function returns the built-in
    default settings provided in the ``cerbere.share`` folder of the package.

    These settings can be customized by defining your own in a new YAML profile
    file and calling the function with ``profile`` argument. If the profile file
    is stored in the user home dir in ``~.cerbere`` folder, providing only the
    file basename is fine, otherwise provide the full path to the profile file.

    A custom file can be defined in YAML, using the following format:

    .. code-block:: yaml

        ---
        # Defines first the global attributes
        attributes:
            # define here a dictionary of global attributes (possibly with
            # default value in the following form
            #
            # with default value
            attr1: val1

            # with no default value (None)
            attr2:

        # Define the variable attributes
        variables:
            # a dictionary of variables containing a dictionary of variable
            # attributes
            variable1:
                varattr1: varval1
                varattr2:

        # Define the encoding attributes, meaningful for a specific format. For
        # instance for NetCDF4, allowed encoding attributes include:
        # scale_factor, add_offset, dtype, least_significant_digit,...
        encoding:
            # a dictionary of variables containing a dictionary of encoding
            # attributes
            variable1:
                scale_factor: 0.01
                add_offset: 273.15
                dtype: int32

    Args:
        profile: the path to (or filename of) the settings profile file

    Returns:
        a dict of attributes and values
    """
    if profile is None:
        profile = 'default_saving_profile.yaml'
    if not os.path.exists(profile):
        # get path from home dir or default
        path = os.path.join(
            os.path.expanduser('~'),
            '.cerbere',
            profile
        )
        if not os.path.exists(path):
            path = os.path.join(
                os.path.dirname(inspect.getfile(inspect.currentframe())),
                'share/{}'.format(profile)
            )
            logging.warning(
                'Using default global attribute file: {}'.format(path)
            )
    else:
        path = profile

    # read attributes
    with open(os.path.abspath(path), 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise

    globattrs = collections.OrderedDict([])
    varattrs = collections.OrderedDict([])
    encoding = collections.OrderedDict([])

    if 'attributes' in config:
        for att in config['attributes']:
            globattrs[att] = config['attributes'][att]
    if 'fields' in config and config['fields'] is not None:
        for v in config['fields']:
            varattrs[v] = config['fields'][v]
    if 'encoding' in config and config['encoding'] is not None:
        for v in config['encoding']:
            encoding[v] = config['encoding'][v]

    return globattrs, varattrs, encoding
