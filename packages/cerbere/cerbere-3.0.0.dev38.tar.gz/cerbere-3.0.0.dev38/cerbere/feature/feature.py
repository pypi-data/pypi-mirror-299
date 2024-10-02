# encoding: utf-8
"""
Abstract class for all data feature objects
"""
from __future__ import absolute_import, division, print_function

import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Mapping, Optional, Tuple

import xarray as xr

from ..dataset.dataset import Dataset
from ..dataset.field import Field

__all__ = ['Feature']


class Feature(Dataset, ABC):
    """
    Abstract class for all **cerbere** feature objects.

    .. |dataset| replace:: :mod:`~cerbere.dataset`
    .. |feature| replace:: :mod:`~cerbere.feature`

    All |feature| classes are inherited from this parent class.

    A feature object is a specialized |dataset| object as it
    can only contains typed observations, where the type is defined by the data
    structure or observation pattern. Being a |dataset| object,
    it can be created from the same arguments as any|dataset| class instance.

    Refer to |dataset|.

    In many cases, a |feature| object will be instantiated from a file content,
    read through a |dataset| class handling the specific format of this file.
    For instance:

    .. code-block:: python

        # let's read gridded data stored in NetCDF following GHRSST format
        # convention. Cerbere provides the GHRSSTNCDataset to read and normalize
        # this type of data.
        from cerbere.dataset.ghrsstncdataset import GHRSSTNCDataset

        ghrsstfile = GHRSSTNCDataset('my_ghrsst_file.nc')

        # map this content into a grid feature object
        gridfeature = Grid(ghrsstfile)

    Args:
        force_reorder (bool): force order of the feature dimensions to match the
            order defined for this feature (True by def.). Improves the level of
            standardization but will involve loading all data in memory in non
            Dask context.
    """
    def __init__(
            self,
            *args,
            force_reorder: Optional[bool]=True,
            **kwargs):
        """
        See:
        Dataset
        """
        super(Feature, self).__init__(*args, **kwargs)

        # check if the object contains coordinate information expected by the
        # current data model
        # check_model() is a virtual method to be implemented
        # by each derived data model class
        if not self._check_dimensions(force_reorder):
            raise ValueError('data structure does not match the feature type')

    @property
    def _dataset_class(self):
        if isinstance(self.dataset, Dataset):
            return self.dataset._dataset_class
        else:
            return 'Dataset'

    @property
    def _base_dataset(self):
        if isinstance(self.dataset, Dataset):
            return self.dataset
        else:
            return super(Feature, self)

    @property
    def _instance_dimname(self):
        raise NotImplementedError

    def __str__(self):
        result = 'Feature : %s\n' % self.__class__.__name__
        result += super(Feature, self).__str__()
        return result

    @property
    def feature_type(self) -> str:
        """Return the type of the feature"""
        return self.__class__.__name__

    @property
    @abstractmethod
    def _feature_geodimnames(self) -> Tuple[str, ...]:
        """The names of the geolocation dimensions defining the feature

        Returns:
            a tuple of geolocation dimension names, using their standard name.
        """
        raise NotImplementedError

    @property
    def geodims(self):
        """Returns the names and sizes of the geolocation dimensions.

        Returns:
            OrderedDict(str, int): a dict where keys as the names of the
                dimensions and the values their respective sizes.
        """
        return OrderedDict([
            (_, self.sizes[_]) for _ in list(self._feature_geodimnames)
            ])

    @abstractmethod
    def get_geocoord_dimnames(
            self, fieldname: str, values: 'xr.DataArray'
            ) -> Tuple[str, ...]:
        """Returns the CF compliant dimension names of a geolocation coordinate
        field.

        Args:
            fieldname (str): the name of the geolocation coordinate, among
                ``lat``, ``lon``, ``time``, ``depth`` or ``height``
            values (DataArray): data array of the coordinate field (used to
                discriminate features with ambiguous dimension sizes, such as
                grid which can have a single time value for all data or a time
                value defined for each pixel)

        Returns:
            tuple of str: the dimension names of the coordinate field

        Note:
            Abstract function to be overridden in each feature class.
        """
        raise NotImplementedError

    def _reorder_geodim(self):
        """check the spatial dimension order is consistent for each variable
        and reorder if necessary.

        Returns:
            tuple: lat and lon dimension names, as found in data vars
        """
        geodims = list(self._feature_geodimnames)
        for v in self._varnames:
            fielddims = list(self.get_field_dims(v))
            dims = [_ for _ in fielddims if _ in geodims]
            if len(dims) == len(geodims):
                if geodims != dims:
                    # re-order
                    logging.warning(
                        'Reordering some dimensions in {}'.format(v)
                    )
                    newdims = geodims + [
                        _ for _ in fielddims if _ not in geodims
                    ]
                    self._std_dataset[v] = self._std_dataset[v].transpose(
                        *newdims,
                        transpose_coords=True
                    )

    def _check_dimensions(self, force_reorder=True):
        """Check that the dataset loaded into the feature fits the required
        properties.

        Verify the existence of the required coordinate fields and dimensions.
        Enforce strict feature dimension order if force_reorder is True (by
        default).

        Args:
            force_reorder (bool): force order of the feature dimensions to match
                the order defined for this feature (True by def.). Improves the
                 level of standardization but will involve loading all data in
                 memory in non Dask context.
        """
        # check required time and space dimensions are in the dataset
        dim_validity = all([
            dim in self.dims
            for dim in self._feature_geodimnames
        ])

        if not dim_validity:
            for dim in self._feature_geodimnames:
                if dim not in self.dims:
                    logging.warning(
                        '  => Missing coordinate dimension: {}'.format(dim)
                    )

        # re-order the required dimensions in the expected order
        if force_reorder:
            self._reorder_geodim()

        return dim_validity

    def append(self,
               feature,
               prefix: str = '',
               add_coords: bool = False,
               as_new_dims: bool = False,
               fields: str = None):
        """Append the fields from another feature

        The fields can share the same coordinates and dimensions (if the added
        feature is an overlay of the current feature). In such case the
        shared coordinates of the added feature are not copied, unless
        `add_coords` is set to True (in which case they are first prefixed
        using `prefix`).

        If the dimensions of the added field have unrelated to the current
        feature (even if they have similar names), `as_new_dims` must be set
        to True. The dimensions (and corresponding coordinates) are prefixed
        with `prefix` and added to with the fields to the current feature.

        Args:
            feature (AbstractFeature derived class): the feature to append.

            prefix (str): prefix to use for naming the fields of the appended
                feature (to avoid conflicts with the existing fields of the
                current feature).

            add_coords: if True, add the feature coordinates as variables. If
                false, they are not added.

            as_new_dims: rename the field and coordinate dimensions with prefix

            fields (list of str): a list of fieldnames specifying which fields
                are to be appended. By default, all fields of the feature are
                appended.
        """
        if as_new_dims and prefix is None:
            raise ValueError(
                'a valid prefix must be provided to rename the dimensions')

        if add_coords and prefix is None:
            raise ValueError(
                'a valid prefix must be provided to add the coordinates')

        added_fields = fields
        if added_fields is None:
            added_fields = feature.fieldnames
        if add_coords:
            added_fields.extend(feature.coordnames)
        added_fields = list(set(added_fields))

        # append fields
        for fieldname in added_fields:
            if fieldname in feature.fieldnames:
                field = feature.get_field(fieldname).clone()
            elif fieldname in feature.coordnames:
                field = feature.get_coord(fieldname).clone()
            else:
                raise ValueError('field {} not found in feature'.format(
                    fieldname))
            field.rename('{}{}'.format(prefix, field.name))

            if as_new_dims:
                # we ensure dim and field names can not be the same (raise an
                # error with xarray
                field._array = field._array.swap_dims(
                    {_: '{}{}'.format(prefix, _) for _ in field.dims})

            self.add_field(field)

    def get_values(self, *args, **kwargs):
        """
        See:
         :meth:`~cerbere.dataset.Dataset.get_values`
        """
        #if 'expand_dims' not in kwargs:
        #    kwargs['expand_dims'] = self._feature_geodimnames
        return super(Feature, self).get_values(
            *args, **kwargs
        )

    def extract(
            self,
            *args,
            bbox=None,
            footprint=None,
            **kwargs) -> 'Feature':
        """Extract a subset as a new ``Feature`` object.

        The subset can be selected through one of the following:
        * bbox: a rectangular lat/lon bounding box.
        * footprint: a more complex shape provided as a lat/lon polygon.
        * index: any valid xarray selection index.

        If none of these are provided, a copy of the whole object is returned.
        The created subset is a new datamodel object of the same class without
        any reference to the source mapper.

        See:
             :func:`~cerbere.dataset.dataset.Dataset.extract`
        """
        if bbox is not None or footprint is not None:
            raise NotImplementedError
        return self.__class__(
            super(Feature, self).extract(*args, **kwargs))

    def extract_field(
            self,
            fieldname: str,
            index: Mapping[str, slice] = None,
            padding: bool = False,
            prefix: str = None,
            **kwargs):
        """
        Create a copy of a field, or subset of a field, and
        padding out as required.

        Args
            fieldname (str): The name of the field to extract.
            index (xarray index type, optional): any kind of xarray indexing

            padding (bool, optional): True to pad out feature with fill values
                to the extent of the dimensions.

            prefix (str, optional): add a prefix string to the field names of
               the extracted subset.
        """
        subset = self._get_xarray_index(index, **kwargs)

        if fieldname in self.coords:
            field = self.coords[fieldname]
        elif fieldname in self.data:
            field = self.data[fieldname]
        else:
            raise ValueError('Unknown field {}'.format(fieldname))

        new_field = Field.to_field(field).clone(subset, padding=padding)
        if prefix is not None:
            new_field.set_name(prefix + field.name)
        return new_field

#         new_dims = copy.copy(field.dimensions)
#         if slices:
#             for dim in new_dims.keys():
#                 if dim in slices:
#                     if not slices[dim].start:
#                         start = 0
#                     else:
#                         start = slices[dim].start
#                     if not slices[dim].stop:
#                         stop = field.dimensions[dim]
#                     else:
#                         stop = slices[dim].stop
#                     new_dims[dim] = stop - start
#
#         elif indices:
#             for dim in new_dims:
#                 if dim in indices:
#                     new_dims[dim] = len(indices[dim])
#
#         new_field = Field(
#             copy.copy(field.variable),
#             new_dims,
#             fields=copy.copy(field.components),
#             datatype=field.datatype
#         )
#         new_field.set_metadata(field.get_metadata())
#         new_field.set_values(
#             field.get_values(slices=slices, indices=indices, padding=padding)
#         )
#         if prefix is not None:
#             new_field.variable.shortname = (prefix +
#                                             new_field.variable.shortname)
#         return new_field
