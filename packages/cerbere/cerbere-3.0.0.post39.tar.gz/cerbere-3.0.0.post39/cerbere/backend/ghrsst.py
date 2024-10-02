from pathlib import Path
import re


import numpy as np
from xarray import open_dataset
from xarray.backends import BackendEntrypoint


class GHRSST(BackendEntrypoint):
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
            decode_times=decode_times, decode_timedelta=decode_timedelta,
            use_cftime=use_cftime, concat_characters=concat_characters,
            decode_coords=decode_coords, drop_variables=drop_variables)

        if 'sst_dtime' in ds.variables and decode_times:
            # replace with new time variable decoding GHRSST time
            dunit = ds.sst_dtime.attrs.get(
                'units', ds.sst_dtime.encoding.get('units'))
            if dunit is None:
                raise ValueError('missing unit for sst_dtime')
            if dunit not in ['second', 'seconds']:
                raise TypeError(
                    'Can not process sst_dtime in {}'.format(dunit)
                )
            reference = np.datetime64(ds['time'].values[0])

            dtime = ds['sst_dtime']

            dtime.attrs = ds['time'].attrs
            dtime.encoding = ds['time'].encoding
            dtime.values = np.ma.array(
                    dtime.values, dtype='timedelta64[s]', copy=False
                ) + reference

            # remove dummy time dimension
            ds = ds.squeeze(dim='time')

            # replace with single time field
            ds = ds.drop_vars(['time'])
            ds = ds.rename({'sst_dtime': 'time'})
            ds = ds.set_coords(['time'])
            if 'comment' in ds['time'].attrs:
                ds['time'].attrs.pop('comment')
            ds['time'].attrs['long_name'] = 'measurement time'

        # normalize collection id (GDS 1.x => 2.x)
        if 'DSD_entry_id' in ds.attrs:
            ds.attrs['id'] = ds.attrs.pop('DSD_entry_id')

        return ds

    open_dataset_parameters = [
        "filename_or_obj", "mask_and_scale", "decode_times",
        "decode_timedelta", "use_cftime", "concat_characters", "decode_coords"]

    def guess_can_open(self, filename_or_obj):
        return re.match(
            r"^[0-9]{8,14}-.*-L[2P|3\w|4]P*_GHRSST-.*nc$",
            Path(filename_or_obj).name) is not None


    description = "Use GHRSST files in Xarray"

    url = "https://link_to/your_backend/documentation"
