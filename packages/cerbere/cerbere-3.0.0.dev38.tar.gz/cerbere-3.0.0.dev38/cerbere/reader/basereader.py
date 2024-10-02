from pathlib import Path
import re
import typing as T

import xarray as xr


class BaseReader:
    """Base class for cerbere readers"""

    pattern: str = None
    engine: str = "netcdf4"
    description: str = "Use <your dataset> files in Xarray"
    url: str = "https://link_to/your_contrib/documentation"

    @classmethod
    def open_dataset(cls, filename_or_obj: T.Union[str, Path], **kwargs):
        ds = xr.open_dataset(filename_or_obj, **kwargs)
        ds.encoding['source'] = filename_or_obj
        ds.encoding['reader'] = cls.__class__.__name__

        return ds

    @classmethod
    def open_mfdataset(
            cls, filename_or_obj: T.List[T.Union[str, Path]], **kwargs):
        ds = xr.open_mfdataset(filename_or_obj, **kwargs)
        ds.encoding['source'] = filename_or_obj
        ds.encoding['reader'] = cls.__class__.__name__

        return ds

    @classmethod
    def guess_can_open(cls, filename_or_obj: T.Union[str, Path]) -> bool:
        return re.match(cls.pattern, Path(filename_or_obj).name) is not None

    @classmethod
    def postprocess(cls, ds, decode_times: bool = True):
        return ds

    @classmethod
    def preprocess(cls, ds: xr.Dataset, **kwargs):
        """called before writing the data

        Put here all transformations required for the data to match given
        format specification associated with the reader
        """
        raise NotImplementedError
