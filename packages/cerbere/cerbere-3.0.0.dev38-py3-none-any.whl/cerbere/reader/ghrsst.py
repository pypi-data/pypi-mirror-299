from pathlib import Path
import re
import typing as T

import numpy as np


class GHRSST:

    pattern: str = re.compile(r"^[0-9]{8,14}-.*-L[2P|3\w|4]P*_GHRSST-.*nc$")
    engine: str = "netcdf4"
    description: str = "Use GHRSST files in Xarray"
    url: str = "https://link_to/your_backend/documentation"

    @staticmethod
    def guess_can_open(filename_or_obj: T.Union[str, Path]) -> bool:
        return re.match(
            GHRSST.pattern,
            Path(filename_or_obj).name) is not None

    @staticmethod
    def postprocess(ds, decode_times: bool = True):
        if "sst_dtime" in ds.variables and decode_times:
            # replace with new time variable decoding GHRSST time
            dunit = ds.sst_dtime.attrs.get(
                "units", ds.sst_dtime.encoding.get("units"))
            if dunit is None:
                raise ValueError("missing unit for sst_dtime")
            if dunit not in ["second", "seconds"]:
                raise TypeError("Can not process sst_dtime in {}".format(dunit))
            reference = np.datetime64(ds["time"].values[0])

            time = ds["sst_dtime"].astype("timedelta64[s]") + reference
            time.attrs = ds["time"].attrs
            time.encoding = ds["time"].encoding

            # remove dummy time dimension
            ds = ds.squeeze(dim="time")

            # replace with single time field
            ds = ds.drop_vars(["time", "sst_dtime"])
            ds['time'] = time.squeeze(dim="time")
            ds = ds.set_coords(["time"])
            if "comment" in ds["time"].attrs:
                ds["time"].attrs.pop("comment")
            ds["time"].attrs["long_name"] = "measurement time"

        # normalize collection id (GDS 1.x => 2.x)
        if "DSD_entry_id" in ds.attrs:
            ds.attrs["id"] = ds.attrs.pop("DSD_entry_id")

        return ds
