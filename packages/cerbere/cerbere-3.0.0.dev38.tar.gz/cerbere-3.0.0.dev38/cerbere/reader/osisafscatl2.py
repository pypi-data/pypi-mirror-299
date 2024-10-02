"""
Reader class for KNMI / OSI SAF scatterometer Level 2 NETCDF files

Example of file pattern:
ascat_20230210_165700_metopc_22116_eps_o_coa_3301_ovw.l2.nc
"""
from pathlib import Path
import re
import typing as T

from .basereader import BaseReader


KNMI_DIMS = {
    'numrows': 'row',
    'NUMROWS': 'row',
    'numcells': 'cell',
    'NUMCELLS': 'cell',
    'NUMAMBIGS': 'solutions',
    'NUMVIEWS': 'views'}


KNMI_VARS = {
    'row_time': 'time',
    'wvc_lat': 'lat',
    'wvc_lon': 'lon'
}


class OSISAFSCATL2(BaseReader):

    pattern = re.compile(r"[a-z]*_[0-9]{8}_[0-9]{6}.*_ovw.l2.nc$")
    engine: str = "netcdf4"
    description: str = "Use OSI SAF NetCDF scatterometer files in Xarray and " \
                   "cerbere"
    url: str = "https://link_to/your_backend/documentation"

    @classmethod
    def postprocess(cls, ds, **kwargs):

        ds = ds.rename_dims(
            {k: v for k, v in KNMI_DIMS.items() if k in ds.dims})
        ds = ds.swap_dims(
            {k: v for k, v in KNMI_VARS.items() if k in ds.variables})

        # normalize longitude to -180/180
        ds['lon'] = ds['lon'].where(ds['lon'] < 180, ds['lon'] - 360)

        return ds
