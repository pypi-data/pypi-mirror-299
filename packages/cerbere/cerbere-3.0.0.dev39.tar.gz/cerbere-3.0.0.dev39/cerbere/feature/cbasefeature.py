# encoding: utf-8
"""
Abstract class for all data feature objects
"""
from __future__ import absolute_import, division, print_function

import logging
import warnings
from abc import ABC, abstractmethod
from collections import OrderedDict
import typing as T

import xarray as xr

import cerbere.accessor.cdataset


__all__ = ['BaseFeature']


class BaseFeature(object):
    """
    Abstract class for all **cerbere** feature objects.

    All |feature| classes are inherited from this parent class.

    A feature object contains a typed xarray |dataset| object
    corresponding to a specific observation pattern. It relies on,
    and sometimes complement, the patterns defined in Climate and Forecast (
    CF) convention. It harmonizes the naming conventions for spatial and
    temporal coordinates, dimensions, etc... and defines methods that can be
    specific to a specific type of feature.

    can only contain typed observations, where the type is defined by the data

    In many cases, a |feature| object will be instantiated from a file content,
    read through the cerbere `open_dataset` method. For instance:

    .. code-block:: python

        # let's read gridded data stored in NetCDF following GHRSST format
        # convention. Cerbere provides a specific engine to read and normalize
        # this type of data.
        import cerbere

        ghrsst_dst = cerbere.open_dataset('my_ghrsst_file.nc', engine='ghrsst')

        # map this content into a grid feature object
        gridfeature = cerbere.feature.Grid(ghrsst_dst)

    Args:
        force_reorder (bool): force order of the feature dimensions to match the
            order defined for this feature (True by def.). Improves the level of
            harmonization but will involve loading all data in memory in non
            Dask context.
    """

    # the expected shape of the coordinates and variables, as defined by CF
    # convention (CF 1.11, Table 9.1)
    cf_canonical_dims = {
        'latitude': None, 'longitude': None, 'vertical': None, 'time': None,
        'data': None
    }
    # optional axes for the feature
    cf_optional_axes = []

    # Unidata Common Data Model provides a longer set of feature types
    cdm_data_type = None

    def __init__(
            self,
            dataset: xr.Dataset,
            force_reorder: bool = True,
            **kwargs):
        """
        See:
        Dataset
        """
        # ensure it is cerberized
        self.dataset = self.cerberize(dataset, force_reorder, **kwargs)

    @classmethod
    def cerberize(
            cls,
            dataset: xr.Dataset,
            force_reorder: bool = True,
            instance_class: 'BaseFeature' = None
    ) -> xr.Dataset:
        """check and modify a dataset so that it fully fits the
        cerbere/CF feature's data model
        """
        # check if the object contains coordinate information expected by the
        # current data model
        # check_model() is a virtual method to be implemented
        # by each derived data model class
        ds = cls._check_dimensions(
            dataset.cb.cfdataset,
            force_reorder=force_reorder,
            instance_class=instance_class)

        # fill in feature type attributes
        if cls.cdm_data_type is not None:
            ds.attrs['cdm_data_type'] = cls.cdm_data_type

        return ds

    @property
    def _instance_dimname(self):
        raise NotImplementedError

    def __str__(self):
        result = 'Feature : %s\n' % self.__class__.__name__
        result += super(BaseFeature, self).__str__()
        return result

    @property
    def ds(self) -> xr.Dataset:
        """The xarray Dataset object composing the feature"""
        return self.dataset

    @ds.setter
    def ds(self, dataset: xr.Dataset):
        self.dataset = dataset

    @property
    def type(self) -> str:
        """the cerbere class name of the feature"""
        return self.__class__.__name__

    @property
    def featureType(self) -> str:
        return self.dataset.attrs.get('featureType')

    @featureType.setter
    def featureType(self, value: str):
        self.dataset.attrs['featureType'] = value

    @classmethod
    def guess_feature(cls, dataset: xr.Dataset) -> T.Optional['BaseFeature']:
        """Guess if the datasets fit the feature's data model.

        Returns:
            the class of the feature, if it's a match. None otherwise.
        """
        return

    # @classmethod
    # def required_dims(cls, *args, **kwargs) -> T.Tuple[str, ...]:
    #     """The names of the geolocation dimensions defining the feature class
    #
    #     Returns:
    #         a tuple of geolocation dimension names, using their standard name.
    #     """
    #     return cls._required_dims

    @property
    def geodims(self):
        """Returns the names and sizes of the geolocation dimensions.

        Returns:
            OrderedDict(str, int): a dict where keys as the names of the
                dimensions and the values their respective sizes.
        """
        return OrderedDict([
            (_, self.dataset.sizes[_]) for _ in list(self.cf_canonical_dims)
            ])

    @abstractmethod
    def get_geocoord_dimnames(
            self, fieldname: str, values: 'xr.DataArray'
            ) -> T.Tuple[str, ...]:
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

    @classmethod
    def _reorder_geodim(cls, dataset: xr.Dataset, instance_class=None) -> \
            xr.Dataset:
        """check the spatial dimension order is consistent for each variable
        and reorder if necessary.

        Returns:
            tuple: lat and lon dimension names, as found in data vars
        """
        geodims = list(cls.cf_canonical_dims)
        ds = dataset.copy(deep=False)
        for v in ds.data_vars:
            fielddims = list(ds[v].dims)
            dims = [_ for _ in fielddims if _ in geodims]
            if len(dims) == len(geodims):
                if geodims != dims:
                    # re-order
                    logging.warning(f'Reordering some dimensions in {v}')
                    newdims = geodims + [
                        _ for _ in fielddims if _ not in geodims
                    ]
                    ds[v] = ds[v].transpose(
                        *newdims,
                        transpose_coords=True
                    )

        return ds

    @classmethod
    def _unexpected_cdm_data_type(cls, cfdst):
        """check Unidata CDM' feature type"""
        return cfdst.cb.cdm_data_type is not None and \
            cls.cdm_data_type is not None and \
            cfdst.cb.cdm_data_type.lower() != cls.cdm_data_type.lower()

    @classmethod
    def _canonical_dims(
            cls, coord: str, *args, **kwargs
    ) -> T.Union[T.Set[str], T.List[T.Set[str]]]:
        return cls.cf_canonical_dims[coord]

    @classmethod
    def is_alias(cls, dataset):
        """Return the class of the parent the feature is an alias for

        Intended for special feature that are a particular implementation of
        an existing feature class (usually a collection), e.g.:
        TrajectoryProfile is an alias for a collection of profiles.
        """
        return

    @classmethod
    def _translate_cf_axis_dim(cls, cf_axis, dataset):
        """return the dimension name in dataset for a canonical CF dimension"""
        dim = dataset.cb.cf_axis_dims.get(cf_axis)
        if dim is not None:
            return dim

        if dataset.cb.cf_instance_dims is not None and len(
                dataset.cb.cf_instance_dims) > 0:
            return dataset.cb.cf_instance_dims[0]

        return cf_axis

    @classmethod
    def _check_feature(cls, dataset, instance_class=None):
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
            instance_class: only for collections
        """
        # required dimensions for dataset coordinates and variables
        if instance_class is not None:
            instance_class = cerbere.feature_class(instance_class)
            required_dims = instance_class.cf_canonical_dims
            cf_optional_coords = instance_class.cf_optional_axes
        else:
            required_dims = cls.cf_canonical_dims
            cf_optional_coords = cls.cf_optional_axes
        required_coords = set(required_dims.keys()) - {'data'}

        # check required spatiotemporal axis coordinates and dimensions are in
        # the dataset
        missing_coords = []
        incorrect_coords = []
        for cf_coord in required_coords:
            if cf_coord not in dataset.cb.cf_coords:
                if cf_coord not in set(cf_optional_coords):
                    missing_coords.append(cf_coord)
                continue

            coord = dataset.cb.cf_coords[cf_coord]

            # ds_canonical_dims = set([
            #     cls._translate_cf_axis_dim(_, dataset)
            #     for _ in cls._canonical_dims(cf_coord, instance_class)])
            #
            # if set(dataset[coord].dims) != ds_canonical_dims:
            #     incorrect_coords.append(coord)

            _c_dims = cls._canonical_dims(cf_coord, instance_class)
            if isinstance(_c_dims, list):
                ds_canonical_dims = [
                    set([cls._translate_cf_axis_dim(_, dataset)
                         for _ in alt]) for alt in _c_dims]
                if all([set(dataset[coord].dims) != _
                        for _ in ds_canonical_dims]):
                    incorrect_coords.append(coord)

            else:
                ds_canonical_dims = set([
                    cls._translate_cf_axis_dim(_, dataset) for _ in _c_dims])
                if set(dataset[coord].dims) != ds_canonical_dims and cf_coord\
                        not in cls.cf_optional_axes:
                    incorrect_coords.append(coord)

        if len(missing_coords) > 0:
            raise cerbere.AxisError(
                f'Data structure does not match the feature type. Missing '
                f'spatiotemporal coordinates: {missing_coords}')

        if len(incorrect_coords) > 0:
            log = ''
            for coord in incorrect_coords:
                log += (
                    f'Data structure does not match the feature type. Axis '
                    f'coordinate {coord} should have dimensions '
                    f'{cls.cf_canonical_dims[cf_coord]}\n')
            raise cerbere.AxisError(log)

    @classmethod
    def _check_dimensions(
            cls, dataset, force_reorder=True, instance_class=None):
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
            instance_class: only for collections
        """
        cls._check_feature(dataset, instance_class=instance_class)

        # # check required spatiotemporal axis coordinates and dimensions are in
        # # the dataset
        # missing_axis_coords = []
        # incorrect_axis_coords = []
        # for coord in required_dims:
        #     if coord not in dataset.cb.cf_axis_coords:
        #         missing_axis_coords.append(coord)
        #     ds_canonical_dims = set([
        #         dataset.cb.cf_axis_dims.get(_, _)
        #         for _ in cls._canonical_dims(coord)])
        #     if (set(dataset[dataset.cb.cf_axis_coords[coord]].dims) !=
        #             ds_canonical_dims):
        #         incorrect_axis_coords.append(coord)
        # if len(missing_axis_coords) > 0:
        #     raise cerbere.AxisError(
        #         f'Data structure does not match the feature type. Missing '
        #         f'axis coordinates: {missing_axis_coords}')
        # if len(incorrect_axis_coords) > 0:
        #     for coord in incorrect_axis_coords:
        #         logging.error(
        #             f'Data structure does not match the feature type. Axis '
        #             f'coordinate {coord} should have dimensions '
        #             f'{cls.cf_canonical_dims[coord]}')
        #     raise cerbere.AxisError(
        #         f'Data structure does not match the feature type.')

        # re-order the required dimensions in the expected canonical order
        if force_reorder:
            return cls._reorder_geodim(dataset, instance_class=instance_class)

        return dataset

    @classmethod
    def _check_dim_sizes(
            cls,
            arr_sizes: T.Dict,
            dims: T.Union[str, T.List[str]],
            sizes: T.Optional[T.Union[int, T.List[int]]] = None):
        if len(arr_sizes) == len(dims) == 0:
            return True

        if set(arr_sizes.keys()) != set(dims):
            return False

        if sizes is not None:
            if isinstance(dims, str):
                if not isinstance(sizes, int):
                    raise ValueError('sizes argument should be an integer')
                return arr_sizes[dims] == sizes

            if isinstance(sizes, int):
                sizes = [sizes] * len(dims)
            for i, dim in enumerate(dims):
                if arr_sizes[dim] != sizes[i]:
                    return False

        return True

    @classmethod
    def _check_coord_dims(
            cls,
            dataset: xr.Dataset,
            axis: str,
            dims: T.Union[str, T.List[str]],
            sizes: T.Optional[T.Union[int, T.List[int]]] = None) -> bool:
        """verify a dataset has a variable with the given dimensions and sizes.
        """
        dst = dataset.cb.cfdataset
        name = dataset.cb.cf_coords.get(axis)

        if name is None:
            return False

        return name in dst.coords and \
            set(dims) == set(dst.coords[name].dims) and \
            cls._check_dim_sizes(dst.coords[name].sizes, dims, sizes)

    def isel(self, *args, **kwargs) -> T.Any:
        """
        shortcut for cerbere ds.cb.isel method but returns the result
        wrapped into a Feature object of the same class as the current object
        """
        return self.__class__(self.ds.cb.isel(*args, **kwargs))

    def copy(self, deep: bool=False):
        return self.__class__(self.ds.copy(deep=deep))
