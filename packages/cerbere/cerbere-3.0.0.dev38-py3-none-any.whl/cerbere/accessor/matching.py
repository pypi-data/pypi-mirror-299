"""
Equivalent terms commonly found in Earth Observation data files from various
providers for Cerbere / CF terms
"""

# common matching dimensions and fields in netCDF files

DIM_MATCHING = {
    'time': 'T',
    'lon': 'X',
    'longitude': 'X',
    'lat': 'Y',
    'latitude': 'Y',
    'x': 'X',
    'y': 'Y',
    'mes': 'station',
    'station': 'station',
    'ni': 'X',
    'cell': 'X',
    'ra_size': 'X',
    'col': 'X',
    'nj': 'Y',
    'row': 'Y',
    'az_size': 'Y',
    'rows': 'Y',
    'columns': 'X',
    'NUMROWS': 'Y',
    'NUMCELLS': 'X',
    'across_track': 'X',
    'along_track': 'Y',
    'TIME': 'T',
    'LATITUDE': 'Y',
    'LONGITUDE': 'X',
    'z': 'Z',
}

COORD_ALIASES = {
    'longitude': {'lon', 'longitude', 'LONGITUDE'},
    'latitude': {'lat', 'latitude', 'LATITUDE'},
    'time': {'TIME'},
    'vertical': {'z'},
}

TIME_COVERAGE_ATTRS = {
    'date': {
        'start': 'start_date',
        'end': 'stop_date'
    },
    'time': {
        'start': 'start_time',
        'end': 'stop_time'
    },
    'time_coverage': {
        'start': 'time_coverage_start',
        'end': 'time_coverage_end'
    },
    'time_coverage2': {
        'start': 'time_coverage_start',
        'end': 'time_coverage_stop'
    },
    'meas_time': {
        'start': 'first_meas_time',
        'end': 'last_meas_time'
    },
}

BBOX_CORNERS = {
    'latmin': [
        'southernmost_latitude', 'geospatial_lat_min', 'south_latitude'
    ],
    'latmax': [
        'northernmost_latitude', 'geospatial_lat_max', 'north_latitude'
    ],
    'lonmin': [
        'westernmost_longitude', 'geospatial_lon_min', 'west_longitude'
    ],
    'lonmax': [
        'easternmost_longitude', 'geospatial_lon_max', 'east_longitude'
    ]
}