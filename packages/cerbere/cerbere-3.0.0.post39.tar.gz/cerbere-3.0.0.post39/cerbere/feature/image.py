# -*- coding: utf-8 -*-
"""
Class for the image feature.
"""
from __future__ import absolute_import, division, print_function

from typing import Tuple

from cerbere.feature.feature import Feature

__all__ = ['Image']


class Image(Feature):
    """
    Feature class for representing a image, a two-dimensional irregular grid
    along the satellite track, with one single time value associated.

    An image feature typically corresponds to a satellite "snapshot" like
    provided typically with a SAR (though technically it is more a swath) or a
    high resolution optical imager: a spatially limited swath section, so small
    that we don't need a time value for each pixel or even scan line. A single
    time value is enough to describe it, as if it was an instant snapshot.
    """
    _feature_geodimnames = 'row', 'cell',

    def __init__(self, *args, **kwargs):
        # create feature
        super(Image, self).__init__(
            *args,
            **kwargs
        )

        # squeeze time dimension in non-coordinate fields
        ctime = self._std_dataset.time.copy()
        if 'time' in self._std_dataset.dims:
            self._std_dataset = self._std_dataset.squeeze(dim='time')
        self._std_dataset.coords['time'] = ctime

    def get_geocoord_dimnames(
            self, fieldname: str,
            values: 'xr.DataArray') -> Tuple[str, ...]:
        if fieldname in ['depth', 'height', 'alt']:
            return 'z',
        elif fieldname == 'time':
            return 'time',
        else:
            return 'row', 'cell',
