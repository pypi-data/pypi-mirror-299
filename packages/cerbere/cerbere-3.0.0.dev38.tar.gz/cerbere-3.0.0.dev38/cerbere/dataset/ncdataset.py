# -*- coding: utf-8 -*-
"""
:mod:`~cerbere.dataset` class to read netCDF files using CF conventions.
"""
from __future__ import absolute_import, division, print_function

import datetime
import logging

from .dataset import Dataset

LOGGER = logging.getLogger()

NETCDF4 = 'NETCDF4'


class NCDataset(Dataset):
    """CF compliant NetCDF Dataset

    Args:
        format ({‘NETCDF4’, ‘NETCDF4_CLASSIC’, ‘NETCDF3_64BIT’,
            ‘NETCDF3_CLASSIC’}, optional): format (default is 'NETCDF4')

    See:
    :class:`~cerbere.dataset.dataset.Dataset`
    """
    def __init__(
            self,
            *args,
            format=NETCDF4,
            **kwargs):
        super().__init__(
            *args,
            format=format,
            **kwargs
        )


    def _convert_format(
        self,
        profile='ghrsst_saving_profile.yaml',
        **kwargs
    ):
        dataset = super()._convert_format(profile, **kwargs)

        # fill in some attributes
        creation_date = datetime.datetime.now()
        dataset.attrs['date_created'] = creation_date
        dataset.attrs['date_modified'] = creation_date
        return dataset

    def get_collection_id(self) -> str:
        """return the identifier of the product collection"""
        if 'id' in self.attrs:
            return self.attrs['id']
