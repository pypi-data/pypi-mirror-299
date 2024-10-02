# -*- coding: utf-8 -*-
"""
:mod:`~cerbere.dataset` class for GHRSST netcdf files
"""
from __future__ import absolute_import, division, print_function

import datetime
import uuid

import cftime
import netCDF4
import numpy
import xarray as xr

from cerbere.dataset import ENCODING, Encoding
from cerbere.dataset.dataset import CDM_TYPES, OpenMode
from cerbere.dataset.ncdataset import NCDataset

from ..cfconvention import DEFAULT_TIME_UNITS

# common matching dimensions and fields in netCDF files
GHRSST_DIM_MATCHING = {
    'time': u'time',
    'lon': u'lon',
    'lat': u'lat',
    'x': u'x',
    'y': u'y',
    'ni': u'cell',
    'nj': u'row'
}


GHRSST_FIELD_MATCHING = {
    'time': u'time',
    'lon': u'lon',
    'lat': u'lat'
}


GHRSST_LEVELS = ['L4', 'L3P', 'L3C', 'L3U', 'L2P']


class GHRSSTNCDataset(NCDataset):
    """
    GHRSST GDS 2.x compliant NetCDF Dataset.
    """
    def __init__(self, *args, **kwargs):
        kwargs['dim_matching'] = GHRSST_DIM_MATCHING
        kwargs['field_matching'] = GHRSST_FIELD_MATCHING
        super().__init__(*args, **kwargs)

    def _open(self, **kwargs):
        # url needs to be opened first in order to guess default datamodel
        super()._open(**kwargs)

        if self._mode != OpenMode.WRITE_NEW:

            # recompose and unpack time variable if required
            self._unsplit_time_coord(
                split_time=('time', 'sst_dtime'), unpack=True
            )

            # normalize collection id (GDS 1.x => 2.x)
            if 'DSD_entry_id' in self.dataset.attrs:
                self.dataset.attrs['id'] = self.dataset.attrs.pop(
                    'DSD_entry_id'
                )

            # fix row/cell ordering (NAVO & AMSRE products)
            if (('NAVO' in self.get_collection_id() and
                 'VIIRS' not in self.get_collection_id()) or
                    self.get_collection_id() == 'USA-RSS-AMSRE-MW-L2-SST'):
                self.dataset.swap_dims({'row': 'cell', 'cell': 'row'})

            # fix lat/lon in MODIS  products
            # @TODO: to be checked
            if (self.get_collection_id() in [
                'JPL-L2P-MODIS_A',
                'MODIS_A-JPL-L2P-v2014.0',
                'JPL-L2P-MODIS_T',
                'MODIS_T-JPL-L2P-v2014.0'
            ]):
                # some lats have nan
                self.dataset['lat'].values = numpy.ma.fix_invalid(
                    self.dataset['lat'].values,
                    copy=False
                )
                # and corresponding lons have 0.0.... !
                self.dataset['lon'].values = numpy.ma.array(
                    self.dataset['lon'].values,
                    mask=self.dataset['lat'].values.mask,
                    copy=False
                )

            # fix lat/lon in NAVO  products
            if 'NAVO' in self.get_collection_id():
                # NAVO lat/lon contains 0 values
                for coord in ['lat', 'lon']:
                    self.dataset[coord].values = numpy.ma.masked_values(
                        self.dataset[coord].values,
                        0,
                        copy=False
                    )

            # @TODO
            #if datamodel is None:
            #    self._feature_type = self.__guess_feature()

    def _unsplit_time_coord(self, split_time, unpack=True):
        """Build a single time fields from two separate fields.

        This address the case of some dataset where each time value is the sum
        of a reference time and an offset. For instance, in GHRSST products,
        the actual pixel time is the sum of``time`` and ``sst_dtime`` fields.
        """
        time_var, dtime_var = split_time

        dataset = self.dataset
        if dtime_var not in dataset.data_vars:
            raise ValueError(
                'Unknown {} field in data fields'.format(dtime_var)
            )
        if time_var not in dataset.coords:
            raise ValueError(
                'Unknown {} field in coordinate fields'.format(time_var)
            )

        dtime = dataset[dtime_var]
        fillvalue = dataset[dtime_var].encoding['_FillValue']
        if 'units' in dtime.attrs:
            dunit = dtime.attrs['units']
        elif 'units' in dtime.encoding:
            dunit = dtime.encoding['units']
        else:
            raise ValueError('missing unit for sst_dtime')
        dtime.attrs = dataset[time_var].attrs
        dtime.encoding = dataset[time_var].encoding
        dtime.encoding[ENCODING][Encoding.IO_FILLVALUE] = fillvalue
        reference = numpy.datetime64(
            dataset[time_var].values[0]
        )
        if unpack:
            if dunit not in ['second', 'seconds']:
                raise TypeError(
                    'Can not process sst_dtime in {}'.format(dunit)
                )
            dtime.values = numpy.ma.array(
                dtime.values, dtype='timedelta64[s]', copy=False
            ) + reference
        else:
            dtime.encoding['add_offset'] = reference

        # remove dummy time dimension
        dataset = dataset.squeeze(dim='time')

        # replace with single time field
        dataset = dataset.drop_vars([time_var])
        dataset = dataset.rename({dtime_var: 'time'})
        dataset = dataset.set_coords([time_var])
        if 'comment' in dataset['time'].attrs:
            dataset['time'].attrs.pop('comment')
        dataset['time'].attrs['long_name'] = 'measurement time'

        # encoding
        dataset['time'].encoding[ENCODING] = {}
        dataset['time'].encoding[ENCODING][Encoding.M_MASK] = \
            numpy.isnat(dataset['time'].values)
        dataset['time'].encoding[ENCODING][Encoding.M_DTYPE] = \
            dataset['time'].dtype

        self.dataset = dataset

    def _convert_format(self,
            profile='ghrsst_saving_profile.yaml',
            force_profile=False,
            **kwargs):
        """Implement specific formatting rules to a dataset.

        Used before saving the dataset to match some specific format
        requirements when writing the dataset on file.
        """
        dataset = super()._convert_format(
            profile=profile, force_profile=force_profile, **kwargs)

        # split time
        if self.__get_level() in set(GHRSST_LEVELS) - set(['L4']):
            reftime = numpy.datetime64(
                self.time_coverage_start.strftime('%Y-%m-%d')
            )
            dtimes = self.get_times() - reftime
            timeattrs=dataset['time'].attrs.copy()
            dataset = dataset.drop('time')
            if self._format == 'NETCDF3_CLASSIC':
                dataset['sst_dtime'] = xr.DataArray(
                    data=dtimes.astype(numpy.int32),
                    dims=dataset['sea_surface_temperature'].dims,
                    coords=dataset.coords
                )
                dataset['sst_dtime'].attrs['units'] = 'seconds'
                origin = numpy.datetime64(
                    cftime.num2date(0, units=DEFAULT_TIME_UNITS)
                )
                dataset['time'] = xr.DataArray(
                    data=numpy.array(
                        [int((reftime - origin).item().total_seconds())]
                    ).astype(numpy.int32),
                    dims=('time',),
                    attrs=timeattrs
                )
                dataset['time'].attrs['units'] = DEFAULT_TIME_UNITS
            else:
                dataset['sst_dtime'] = xr.DataArray(
                    data=dtimes,
                    dims=dataset['sea_surface_temperature'].dims,
                    coords=dataset.coords
                )
                dataset['sst_dtime'].encoding['units'] = 'seconds'
                dataset['time'] = xr.DataArray(
                    data=[reftime],
                    dims=('time',),
                    attrs=timeattrs
                )
                dataset['time'].encoding['units'] = DEFAULT_TIME_UNITS
            dataset['time'].attrs['long_name'] = 'reference time of sst file'
            dataset['sst_dtime'].attrs['long_name'] = \
                'time difference from reference time'

            # fill in specific GHRSST attributes
        dataset.attrs['netcdf_version_id'] = netCDF4.getlibversion()

        dataset.attrs['uuid'] = str(uuid.uuid1())
        dataset.attrs['date_modified'] = datetime.datetime.now()
        dataset.attrs['date_issued'] = dataset.attrs['date_modified']
        dataset.attrs['date_metadata_modified'] = dataset.attrs['date_modified']
        dataset.attrs['geospatial_bounds'] = self.wkt_bbox

        for k, v in dataset.data_vars.items():
            if 'time' not in v.dims:
                dataset[k] = v.expand_dims('time', axis=0).assign_coords(
                    {'time': dataset.time}
                )

        return dataset

    def __get_level(self):
        id = self.get_collection_id()
        if id is None:
            raise ValueError(
                'The dataset object is missing the required id attribute'
            )
        for _ in GHRSST_LEVELS:
            if _ in id:
                return _
        raise ValueError(
            'Could not determine the product type for {}'
            .format(self.get_collection_id())
        )

    def __guess_feature(self):
        """Return the detected feature type"""
        attrs = self.read_global_attributes()
        if 'cdm_data_type' in attrs:
            val = self.read_global_attribute('cdm_data_type')
            if val not in CDM_TYPES:
                raise ValueError('Unknown cdm feature type {}'.format(val))
            return CDM_TYPES[val]

        elif 'L2' in self.get_collection_id():
            return 'Swath'
        elif ('L3' in self.get_collection_id() or
                'L4' in self.get_collection_id()):
            return 'Grid'
        else:
            raise ValueError('Could not guess feature type')

    #
    # def read_values(self, fieldname,**kwargs):
    #     return super().read_values(fieldname, **kwargs)

#
#         # ==========================================================
#         try:
#             if fieldname == 'time' and \
#                     'sst_dtime' in self.source().variables:
#                 ncvarname = 'sst_dtime'
#             else:
#                 ncvarname = fieldname
# #             if fieldname not in ['lat', 'lon']:
# #                 # GHRSST products have a time dimension which is not part of
# #                 # cerbere data model
# #                 if slices is not None and len(slices) == 2 and\
# #                         'bnds' not in fieldname:
# #                     slices.insert(0, 0)
#             if self.__is_reversed():
#                 # case where row and cells are reversed
#                 if slices:
#                     if len(slices) == 2:
#                         newslices = [slices[1], slices[0]]
#                     else:
#                         newslices = slices
#                     newslices = tuple(newslices)
#                 else:
#                     newslices = slices
#                 values = super(GHRSSTNCDataset, self).read_values(ncvarname,
#                                                                   newslices)
#                 if len(values.shape) == 2:
#                     values = numpy.ma.transpose(values)
#             elif (fieldname == 'lon' or fieldname == 'lat') and \
#                     len(self.source().variables[fieldname].shape) == 3:
#                 # case where the lat/lon have a time dimension (ARC ATSR files)
#                 if slices is not None:
#                     new_slices = slices
#                     new_slices.insert(0, 0)
#                     values = super(GHRSSTNCDataset, self).read_values(ncvarname,
#                                                                       tuple(new_slices))
#                 else:
#                     values = super(GHRSSTNCDataset, self).read_values(ncvarname,
#                                                                       slices)
#                     if values.ndim == 3:
#                         values = values[0, :, :]
#             else:
#                 values = super(GHRSSTNCDataset, self).read_values(
#                     ncvarname,
#                     slices)
#             if self.__is_reversed()\
#                     and (fieldname == 'lon' or fieldname == 'lat'):
#                 # NAVO lat/lon contains 0 values
#                 if 'NAVO' in self.get_collection_id():
#                     values = numpy.ma.masked_equal(values, 0, atol=0.0001,
#                                                    copy=False)
#             # homogenize longitudes
#             if fieldname == 'lon':
#                 ind = numpy.ma.where(values >= 180.)
#                 values[ind] = values[ind] - 360.
#                 ind = numpy.ma.where(values < -180.)
#                 values[ind] = values[ind] + 360.
#             if ncvarname == 'sst_dtime':
#                 # pixel time is time + sst_dtime
#                 var = self.source().variables['time']
#                 values = var[0] + values
#             # fix invalid values
#             if (self.get_collection_id() in ['JPL-L2P-MODIS_A',
#                                              'MODIS_A-JPL-L2P-v2014.0',
#                                              'JPL-L2P-MODIS_T',
#                                              'MODIS_T-JPL-L2P-v2014.0']):
#                 # some lats have nan
#                 if fieldname == 'lat':
#                     values = numpy.ma.fix_invalid(values, copy=False)
#                 # and corresponding lons have 0.0.... !
#                 elif fieldname == 'lon':
#                     lats = self.read_values('lat', slices=slices)
#                     lats = numpy.ma.fix_invalid(lats, copy=False)
#                     values = numpy.ma.array(values, mask=lats.mask,
#                                             copy=False)
#             return values
#         except:
#             logging.error("Could not read values for fieldname: {}".format(
#                 fieldname
#             ))
#             raise
#
#
