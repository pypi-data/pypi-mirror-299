# -*- coding: utf-8 -*-
"""
BackendEntrypoint class for KNMI / OSI SAF scatterometer Level 2 NETCDF files
"""
import os

import numpy as np
from xarray import open_dataset
from xarray.backends import BackendEntrypoint


class OSISAFSCATL2(BackendEntrypoint):
    def open_dataset(
        self,
        filename_or_obj,
        mask_and_scale=True,
        decode_times=True,
        decode_timedelta=True,
        use_cftime=True,
        concat_characters=True,
        decode_coords=True,
        drop_variables=None,
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ):
        ds = open_dataset(
            filename_or_obj, mask_and_scale=mask_and_scale,
            decode_times=True, decode_timedelta=decode_timedelta,
            use_cftime=False, concat_characters=concat_characters,
            decode_coords=decode_coords, drop_variables=drop_variables)

        ds.cb.cerberize(
            dim_matching={
                'numrows': 'row',
                'NUMROWS': 'row',
                'numcells': 'cell',
                'NUMCELLS': 'cell',
                'NUMAMBIGS': 'solutions',
                'NUMVIEWS': 'views'
            },
            var_matching={
                'row_time': 'time',
                'wvc_lat': 'lat',
                'wvc_lon': 'lon'
            }
        )

        return ds.cb.cfdataset

    open_dataset_parameters = [
        "filename_or_obj", "mask_and_scale", "decode_times",
        "decode_timedelta", "use_cftime", "concat_characters", "decode_coords"]

    def guess_can_open(self, filename_or_obj):
        try:
            _, ext = os.path.splitext(filename_or_obj)
        except TypeError:
            return False
        return ext in {".nc"}

    description = "Use OSI SAF NetCDF scatterometer files in Xarray and cerbere"

    url = "https://link_to/your_backend/documentation"
