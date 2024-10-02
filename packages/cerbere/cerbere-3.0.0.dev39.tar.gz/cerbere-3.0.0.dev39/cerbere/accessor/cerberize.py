"""
A collection of functions to harmonize Xarray Dataset and DataArray objects
wrt to CF and other conventions
"""
import datetime
import dateutil.parser as parser
from itertools import chain
import logging
import typing as T
import warnings

import numpy as np
import xarray as xr

import cerbere
import cerbere.cfconvention as cf
import cerbere.accessor.matching as match
from cerbere.feature.cdiscretefeature import DiscreteFeature


# key of Dataset encoding attribute for identified CF Coordinates
CB_COORDS = '_cb_coords'

# key of Dataset encoding attribute for dimensions being axes
CB_AXIS_DIMS = '_cb_axis_dims'

#
CB_AXIS_COORDS = '_cb_axis_coords'

# key of Dataset encoding attribute for dimensions being instance axes in a
# discrete feature collection
CB_INSTANCE_DIMS = '_cb_instance_dims'

# key of Dataset encoding attribute for coordinates being instance axes in a
# discrete feature collection
CB_INSTANCE_COORDS = '_cb_instance_coords'

# key of encoding attribute set when Dataset object was harmonized with cerbere
CB_CERBERIZED = '_cb_is_cerberized'


def _cerberize(
        dst: xr.Dataset,
        dim_matching: T.Optional[T.Dict[str, str]] = None,
        coord_matching: T.Optional[T.Dict[str, str]] = None,
        attr_matching: T.Optional[T.Dict[str, str]] = None,
        axis_coordinates: T.Optional[T.Dict[str, str]] = None) -> xr.Dataset:
    """apply some transformation to original dataset to make it more
    convention compliant (CF 1.7+).

    Args:
        coord_matching (dict): explicitly provides the matching between file
            native coordinate vars (keys) and their expected Cerbere/CF
            equivalent (values).
        axis_coordinates(dict): explicitly provide the matching between
          CF spatiotemporal axis dimensions (X, Y, Z, T) and the
          coordinate variables in the dataset.
        attr_matching (dict): explicitly provides the matching between file
            native attributes (keys) and their expected Cerbere/CF
            equivalent (values).
    """
    # first modify the dataset according to the method arguments
    if dim_matching is not None:
        dst = dst.swap_dims(dim_matching)

    if coord_matching is not None:
        dst = dst.rename(coord_matching)

    if axis_coordinates is not None:
        for axis in axis_coordinates:
            dst[axis_coordinates[axis]].cb.axis = axis

    if attr_matching is not None:
        for attr, new_attr in attr_matching.items():
            dst.attrs[new_attr] = attr

    # store found CF axis dimensions
    if CB_AXIS_DIMS not in dst.encoding:
        dst.encoding[CB_AXIS_DIMS] = {}
    if CB_AXIS_COORDS not in dst.encoding:
        dst.encoding[CB_AXIS_COORDS] = {}
    if CB_INSTANCE_DIMS not in dst.encoding:
        dst.encoding[CB_INSTANCE_DIMS] = []
    if CB_INSTANCE_COORDS not in dst.encoding:
        dst.encoding[CB_INSTANCE_COORDS] = []

    # verify and make compliant spatiotemporal coordinates and dimensions
    dst = _cerberize_coords(dst)
    dst = _cerberize_dims(dst)

    # guess discrete instance dim
    # detect in the dimensions of CF coordinates the ones that don't
    # correspond to spatiotemporal dimensions
    # instance_dim = {}
    # for c in cf.GEOCOORDS:
    #     coord = self._cfdataset[c]
    #     if coord is None:
    #         assert c == 'vertical'
    #         continue
    #
    #     instance_dims = set(coord.dims) - {'time', self.Z, 'lat', 'lon',
    #                                        'cell', 'row', 'ni', 'nj'}
    #     if len(instance_dims) != 0:
    #         instance_dim = instance_dim.union(instance_dims)
    #     # @TODO

    # guess coordinate axis
    # self._cfdataset = self._cfdataset.cf.guess_coord_axis(verbose=False)

    # set lat, lon, time as coordinates and complete metadata to match CF
    # model
    for coord in dst.encoding[CB_COORDS]:

        # ensure it is set as coordinate
        if coord in dst.variables:
            if coord not in dst.coords:
                dst = dst.set_coords([coord])
            coordvar = dst.coords[coord]

        # axis coordinate => set axis attribute
        reverse_axis_dims = {
            v: k for k, v in dst.encoding[CB_AXIS_DIMS].items()}
        if coord in reverse_axis_dims:
            dst[coord].attrs['axis'] = reverse_axis_dims[coord]

        # if coordinate has no spatiotemporal dimensions and there is no
        # other variable corresponding to the same axis, then it must be an
        # axis coordinate
        # if len(coord.dims) == 0:
        #     # @TODO check CF convention about this
        #     if ('axis' not in coordvar.attrs
        #             or coordvar.attrs['axis'] not in cf.CF_COORD_AXIS.values()):
        #         coordvar.attrs['axis'] = cf.CF_COORD_AXIS[coord]

    # verify _FillValue and standardize
    for v in dst.variables:
        # replace missing_value with _FillValue
        if 'missing_value' in dst.variables[v].encoding:
            if '_FillValue' in dst.variables[v].encoding:
                dst.variables[v].encoding.pop('missing_value')
            else:
                dst.variables[v].encoding['_FillValue'] = \
                    dst.variables[v].encoding.pop('missing_value')

    # harmonize attributes
    dst = _cerberize_attrs(dst)

    # update coordinates attribute of data variables
    dst = update_cf_coordinates_attr(dst)

    # check geolocation coordinates are defined and valid
    if not _check_mandatory_geocoordinates(dst):
        raise ValueError(
            'The dataset is not a valid observation set or is malformed.'
        )

    # mark as cerberized
    dst.encoding[CB_CERBERIZED] = True

    return dst


def _check_mandatory_geocoordinates(dst: xr.Dataset) -> bool:
    """check if the required CF spatiotemporal coordinates are in the
    dataset
    """
    ok = True
    for coord in cf.CF_REQ_GEOCOORDS:
        try:
            _ = _guess_cf_coord(dst, coord)
        except cerbere.CoordinateError as e:
            logging.exception(e)
            logging.warning(
                '  => Missing coordinate var: {}'.format(coord))
            ok = False

    return ok


def _cerberize_dims(dst: xr.Dataset) -> xr.Dataset:
    """Guess and harmonize the spatio-temporal axis dimensions
    """
    cf_axis_dims, cf_axis_coords, cf_instance_dims, = _guess_cf_axes(dst)

    # rename axis dimension to coordinate name if unidimensional, and set
    # axis attribute
    for axis, coord in cf_axis_coords.items():
        if (len(dst[coord].dims) == 1 and
                len(cf_axis_dims) > 0 and
                axis in cf_axis_dims and
                cf_axis_dims[axis] != coord):
            if cf_axis_dims[axis] in cf_instance_dims:
                # TODO do sth clearer here
                continue
            logging.debug(
                f'Renaming axis dimension {axis} to {coord} as it is an '
                f'axis coordinate')
            # dst = dst.swap_dims({cf_axis_dims[axis]: coord})
            # bug issue on swap_dims, replace above with rename :
            # https://github.com/pydata/xarray/issues/9542#issuecomment
            # -2372117209
            dst = dst.rename({cf_axis_dims[axis]: coord})
            cf_axis_dims[axis] = coord

        # if dst[coord].cb.axis is None:
        #     dst.cb.set_axis(coord, cf_axis_dims[axis])

    # rename instance dimension if any
    if len(cf_instance_dims) > 1:
        raise NotImplementedError

    if len(cf_instance_dims) == 1:
        ftype = dst.attrs.get('featureType')
        if ftype is not None:
            feat_class = cerbere.class_by_cf_feature_type(ftype)
            if feat_class.cf_element_instance_axis is None:
                i_axis = feat_class.cf_instance_axis
            else:
                i_axis = feat_class.cf_element_instance_axis
            if i_axis is not None and cf_instance_dims[0] != i_axis:
                logging.debug(f'Renaming instance axis {cf_instance_dims[0]} '
                              f'to {i_axis}')
                dst = dst.swap_dims({cf_instance_dims[0]: i_axis})
        else:
            i_axis = cf_instance_dims[0]

        dst.encoding[CB_INSTANCE_DIMS] = (i_axis,)

    # name = None
    # for cfname in cf.CF_AXIS:
    #     try:
    #         name = self._guess_cf_axis(self._cfdataset, cfname)
    #     except CoordinateError:
    #         if cfname == 'vertical':
    #             logging.debug('No coordinate found for vertical axis')
    #         else:
    #             raise

    reduced = {}
    for dim in dst.dims:
        if dim in match.DIM_MATCHING:
            if dim == match.DIM_MATCHING[dim]:
                continue
            if match.DIM_MATCHING[dim] in dst.dims:
                if match.DIM_MATCHING[dim] in match.DIM_MATCHING:
                    continue
                raise ValueError(
                    'Attempt to rename a dimension with the same name as an'
                    ' already existing dimension, without permutation name '
                    'provided : {} <=> {}'.format(dim, match.DIM_MATCHING[dim]))
            reduced[dim] = match.DIM_MATCHING[dim]

    dst.encoding[CB_AXIS_DIMS] = cf_axis_dims
    dst.encoding[CB_AXIS_COORDS] = cf_axis_coords

    return dst
#    return dst.swap_dims(reduced)


def _cerberize_coords(dst) -> xr.Dataset:
    """
    Guess and harmonize the spatio-temporal coordinate variables
    """
    # store found coordinates
    if '_cb_coords' not in dst.encoding:
        dst.encoding[CB_COORDS] = {}

    name = None
    for cfname in cf.CF_COORDS:
        try:
            name = _guess_cf_coord(dst, cfname)
        except cerbere.CoordinateError:
            if cfname == 'vertical':
                logging.debug('No coordinate found for vertical axis')
                continue
            else:
                raise

        # rename latitude/longitude/time to Cerbere convention: lat, lon, time
        # z coordinate is not renamed but accessible through property `vertical`
        cb_name = cf.CB_COORD_CONVENTION.get(cfname, name)
        if cb_name != name:
            dst = dst.rename_vars({name: cb_name})

        # fill in missing attributes
        if cfname in cf.GEOCOORD_ATTRS:
            for attr, val in cf.GEOCOORD_ATTRS[cfname].items():
                if attr not in dst[cb_name].attrs:
                    dst[cb_name].attrs[attr] = val

        # memorize found coordinates
        dst.encoding[CB_COORDS][cfname] = cb_name

        # set as a dataset coordinate
        if cb_name not in dst.coords:
            dst = dst.set_coords(cb_name)

    # check all mandatory coordinates found
    for coord in cf.CF_REQ_GEOCOORDS:
        if coord not in dst.encoding[CB_COORDS]:
            raise cerbere.CoordinateError(
                f'Mandatory coordinate {coord} was not found in this '
                f'dataset')

    # # rename variables wrt to a dictionary of aliases. By default the
    # # aliases correspond to frequently met variant of spatial and
    # # temporal coordinate names
    # reduced = {}
    # for v in self._cfdataset.variables:
    #     if v in var_matching:
    #         if v == var_matching[v]:
    #             continue
    #         if var_matching[v] in self._cfdataset.variables:
    #             if var_matching[v] in var_matching:
    #                 continue
    #             raise ValueError(
    #                 'Attempt to rename a variable with the same name as an'
    #                 ' already existing variable, without permutation name '
    #                 'provided : {} <=> {}'.format(v, var_matching[v]))
    #
    #         reduced[v] = var_matching[v]
    #
    # self._cfdataset = self._cfdataset.rename_vars(reduced)

    # # guess axis coordinates
    # if self._cfdataset.encoding.get('cf_axes') is None:
    #     self._cfdataset.encoding['cf_axes'] = (
    #         DatasetAccessor._guess_cf_axes(self._cfdataset))
    #
    # # find spatial and temporal coordinate variables
    # for axis in ['X', 'Y', 'T', 'Z']:
    #     if axis in self._cfdataset.data_vars and \
    #             len(self._cfdataset.data_vars[axis]) == 1:
    #         pass

    return dst


def _cerberize_attrs(
        dst: xr.Dataset,
        attr_matching: T.Optional[T.Dict[str, str]] = None):
    """decode the standard attributes

    Possibly change the name of some attributes to harmonize them to
    Cerbere CF/ACDD convention, based on an internal dict of known variants.
    """
    if attr_matching is not None:
        for stdattr, attr in attr_matching.items():
            dst.attrs[stdattr] = dst.attrs.pop(attr)

    _cerberize_time_coverage(dst)

    return dst


def _cerberize_time_coverage(dst: xr.Dataset):
    """decode time coverage attributes and update the translation table"""
    try:
        dt = _decode_time_coverage_attr(dst, 'start')
        if dt is not None:
            dst.attrs['time_coverage_start'] = dt
        dt = _decode_time_coverage_attr(dst, 'end')
        if dt is not None:
            dst.attrs['time_coverage_end'] = dt
    except (TypeError, ValueError) as e:
        logging.error(f'error when trying to get the time coverage from '
                      f'attributes; {str(e)}')
    except:
        raise


def _decode_time_coverage_attr(
        dst: xr.Dataset, boundary: str) -> datetime.datetime:
    """Convert start/end time attributes to Cerbere/CF convention (
    time_coverage_start/time_coverage_end), attempting different existing
    conventions.

    Args:
        boundary(str): type of date attribute (`start` or `end`)

    Returns:
        datetime: start/end time of the data in file.
    """
    attrs = dst.attrs

    # time_coverage_start/end
    for attrstyle in match.TIME_COVERAGE_ATTRS:
        attrdate = match.TIME_COVERAGE_ATTRS[attrstyle][boundary]
        if attrdate in attrs:
            if isinstance(attrs[attrdate], datetime.datetime):
                return attrs.pop(attrdate)
            return parser.parse(attrs.pop(attrdate))

    # combination of two time/date attributes (such as start_date and
    # start_time)
    attrdate = match.TIME_COVERAGE_ATTRS['date'][boundary]
    if attrdate in attrs:
        if match.TIME_COVERAGE_ATTRS['time'][boundary] in attrs:
            # start/end_time/date combination
            attrtime = attrs.pop(
                match.TIME_COVERAGE_ATTRS['time'][boundary])
            return parser.parse(f'{attrs.pop(attrdate)}T{attrtime}')

        return parser.parse(attrs.pop(attrdate))


def update_cf_coordinates_attr(dst: xr.Dataset) -> xr.Dataset:
    """Update the "coordinates" attribute of data variable according to CF
    rules.
    """
    aux_coords = guess_cf_aux_coords(dst)

    if len(aux_coords) > 0:
        for v in dst.data_vars:
            coordinates = []
            for aux, adims in aux_coords.items():
                if len(set(dst[v].dims).intersection(set(adims))) > 0:
                    coordinates.append(aux)
            if len(coordinates) > 0:
                if ('coordinates' in dst[v].encoding
                        and set(dst[v].encoding['coordinates'].split(' ')) !=
                        set(coordinates)):
                    warnings.warn(
                        f'The current value of "coordinates" attribute of '
                        f'variable {v} does not equal what was inferred by '
                        f'cerbere: '
                        f'{set(dst[v].encoding["coordinates"].split(" "))} <> '
                        f'{set(coordinates)}')
                    continue
                dst[v].encoding['coordinates'] = ' '.join(coordinates)

    return dst


def guess_cf_aux_coords(dst: xr.Dataset) -> dict[T.Any, tuple[T.Hashable, ...]]:
    """Guess the spatiotemporal coordinates of a dataset, among longitude,
    latitude, vertical or time, which depends on more than one spatiotemporal
    dimension"""
    aux_coords = {}
    for coord in dst.encoding[CB_COORDS].values():
        if len(dst[coord].dims) > 1:
            aux_coords[coord] = dst[coord].dims

    return aux_coords


def _guess_cf_coord_on_units(
        dst: xr.Dataset,
        name: str) -> T.Set[T.Hashable]:
    if name == 'time':
        return {
            _ for _ in dst.variables
            if ('units' in dst[_].attrs and dst[_].attrs['units'] is str and
               dst[_].attrs['units'].startswith('since '))
               or np.issubdtype(dst[_].dtype, np.datetime64)}

    if name not in cf.CF_COORD_UNITS:
        # currently difficult to identify Z axis as many units possible
        # which can be confused with other quantities
        return set()

    return {
        _ for _ in dst.variables
        if 'units' in dst[_].attrs and
           dst[_].attrs['units'] in cf.CF_COORD_UNITS[name]}


def _guess_cf_coord_on_std_name(
        dst: xr.Dataset,
        name: str) -> T.Set[T.Hashable]:
    cf_std_name = cf.GEOCOORD_STD_NAME[name]
    matches = {
        _ for _ in dst.variables.keys()
        if dst[_].attrs.get('standard_name') in cf_std_name}
    if len(matches) > 1:
        logging.warning(
            f'There are more than one variable with a standard name '
            f'matching a possible {name} coordinate. The coordinate for '
            f'this axis may not be identified and '
            f'it will probably require a specific reader to fix this '
            f'dataset.')

    return matches


def _guess_cf_coord_on_alias(
        dst: xr.Dataset,
        name: str) -> T.Set[T.Hashable]:
    # look for aliases
    return {
        _ for _ in dst.variables.keys() if _ in match.COORD_ALIASES[name]}


def _guess_axis_coord(dst: xr.Dataset, axis: str) -> T.List[T.Hashable]:
    """Guess the coordinate variable corresponding to a given axis attribute
    in a Dataset

    Args:
        dst: Dataset
        axis: CF coordinate axis name (X, Y, Z, T)

    Return:
        the list of variable names matching the coordinate axis in the Dataset
    """
    coords = [
        _ for _ in dst.variables.keys() if dst[_].attrs.get('axis') == axis]
    if len(coords) > 1:
        warnings.warn(
            f'There are more than one variable with attribute axis'
            f' {axis}: {coords}. There must be only one in a CF compliant '
            f'file. The coordinate for this axis may not be identified and '
            f'it will probably require a specific reader to fix this '
            f'dataset.', cerbere.CWarning)

    return coords


def _guess_cf_coord_on_axis(
        dst: xr.Dataset,
        name: str) -> T.List[T.Hashable]:
    """Guess geocoordinate (latitude, longitude, time or vertical) variable
    based on axis attribute"""
    return _guess_axis_coord(dst, cf.CF_COORD_AXIS[name])


def _guess_cf_coord(
        dst: xr.Dataset,
        name: str) -> T.Hashable:
    """.
    Find in the dataset the corresponding coordinate name for a CF
    standard spatiotemporal coordinate.

    The search is based on, in order of priority:
    * the units of the dataset variables
    * the standard name attribute of the dataset variables
    * the matching with a list of common aliases for the CF
      spatiotemporal coordinates
    """
    # search based on units
    units = _guess_cf_coord_on_units(dst, name)

    # search a variable with a matching standard name for the given
    # coordinate
    std_attr = _guess_cf_coord_on_std_name(dst, name)

    # look for aliases
    aliases = _guess_cf_coord_on_alias(dst, name)

    # look for axis variables
    axes = set(_guess_cf_coord_on_axis(dst, name))

    # attempt different selection strategies
    candidates = units.union(std_attr, aliases, axes)

    if len(candidates) == 0:
        if name in dst.variables:
            return name
        raise cerbere.CoordinateError(
            f'No candidate variable for coordinate {name}')

    if len(candidates) == 1:
        # agreement of all criteria
        return candidates.pop()

    for cname in [name, cf.CB_COORD_CONVENTION.get(name)]:
        if cname in dst.variables and cname in candidates:
            return cname

    # repeated unique candidate ?
    repeated = candidates
    for _ in [units, std_attr, aliases, axes]:
        if len(_) != 0:
            repeated = repeated.intersection(_)
    if len(repeated) == 1:
        return repeated.pop()

    # ambiguous case
    logging.warning(
        f'several candidate variables for coordinate {name}: '
        f'{repeated}.')

    if len(axes) == 1:
        # precedence of axis information
        logging.warning(f'selecting {list(axes)[0]} as coordinate {name} based '
                        f'on axis indication')
        return list(axes)[0]

    if len(units.union(std_attr)) == 1:
        logging.warning(f'selecting {list(units.union(std_attr))[0]} as '
                        f'coordinate {name} based on units and/or standard '
                        f'attribute indication')
        return units.union(std_attr).pop()

    raise cerbere.CoordinateError(
        f'several candidate variables for coordinate {name}: {aliases}')

#
# def get_geocoord_by_axis(dst: xr.Dataset, axis: str) -> xr.DataArray:
#     """Return the geolocation coordinate variable for the given axis.
#     """
#     axis = dst.coords[dst.cb.axis_coordname(axis)]
#
#     if axis is None:
#         raise cerbere.AxisError(f'No coordinate for {axis} axis')
#
#     return axis
#
#
# def axis_coordname(dst: xr.Dataset, axis: cf.CF_AXIS) -> str:
#     """Returns the name of the spatiotemporal coordinate associated
#     with a given CF axis.
#
#     Args:
#         axis: axis name among 'X', 'Y', 'T', 'Z'
#     """
#     if axis not in cf.CF_AXIS:
#         raise cerbere.AxisError(
#             '{} is not a geolocation coordinate'.format(axis))
#
#     for coordname in self.geocoordnames:
#         if self._cfdataset.coords[coordname].attrs['axis'] == axis:
#             if len(self._cfdataset.coords[coordname].dims) > 1:
#                 logging.warning(
#                     f'The variable {coordname} has an axis attribute with'
#                     f' value {axis} but it can not be an axis as it has '
#                     f'more than one dimension. The file or Dataset object '
#                     f'should be fixed first.')
#             else:
#                 return coordname
#
#     raise cerbere.AxisError('No coordinate found for axis: {}'.format(axis))


def _set_axis(dst: xr.Dataset, name: str, axis: str):
    """Set a variable as a CF axis.

    Args:
        name: name of the variable to set as an axis
        axis: value of the axis
    """
    if axis not in cf.CF_AXIS:
        raise cerbere.AxisError(f'Illegal axis {axis}')

    # verify there is no variable with this axis already
    axis_vars = set(
        [dst[_].name for _ in dst.variables
         if 'axis' in dst[_].attrs and dst[_].attrs['axis'] == axis]) - {name}
    if len(axis_vars) > 0:
        raise cerbere.AxisError(
            f'Axis {axis} is already set for variable(s) {axis_vars}. '
            f'Only one coordinate variable is possible for a given axis.')

    dst[name].attrs['axis'] = axis


def _guess_cf_instance_coord(dst: xr.Dataset) -> T.Optional[T.Hashable]:
    """the name of the instance variable, holding the `cf_role`
    attribute

    One-dimensional variables in a Discrete Geometry CF file, which have
    only the instance dimension as dimension (such as x(i), y(i) and z(i)
    for a timeseries), are instance variables. Instance variables provide
    the metadata that differentiates individual features.
    """
    cf_role_vars = [v for v in dst.variables if 'cf_role' in dst[v].attrs]

    if len(cf_role_vars) == 1:
        return cf_role_vars[0]

    if len(cf_role_vars) == 2:
        # possible for
        # @TODO
        pass

    if len(cf_role_vars) > 2:
        raise cerbere.CoordinateError(
            f'There are multiple variables with `cf_role` attribute. It '
            f'seems like a non-compliance'
        )

    dst.encoding[CB_INSTANCE_COORDS] = cf_role_vars


def _guess_cf_instance_dim(dst: xr.Dataset) -> T.Optional[T.Hashable]:
    """the instance dimension of the dataset, if any.

    The instance dimension is the dimension that identifies a particular
    feature within a collection of features in CF convention.

    Instance dimensions may be provided for CF data models such as:
      - Profile
      - Collections
    """
    inst_var = _guess_cf_instance_coord(dst)

    # instance variable is defined
    if inst_var is not None:
        if len(dst[inst_var].dims) > 1:
            raise ValueError('A CF instance variable should have only '
                             'zero or one dimension')
        if len(dst[inst_var].dims) == 1:
            return dst[inst_var].dims[0]

    # check among instance dim names known in CF convention for
    # different feature types if one is present in the dataset dims
    # (profile, station, trajectory,...)
    for feat_class in cerbere.helpers._feature.values():
        if not isinstance(feat_class, DiscreteFeature):
            return
        axis = feat_class.load().cf_instance_axis
        if axis in dst.dims:
            return axis


def _guess_explicit_axis_coordinates(
        dst: xr.Dataset) -> T.Tuple[T.Dict, T.Dict]:
    """guess and return the axis coordinates with explicit axis attribute

    Return:
        a tuple of two dictionaries where keys are the CF axes (X, Y, Z or T)
        and values, respectively, the corresponding axis coordinate variable
        names and axis coordinate dimensions.
    """
    cf_axis_coords = {}
    cf_axis_dims = {}

    for axis in cf.GEOCOORD_AXIS.values():
        axis_attr_coords = _guess_axis_coord(dst, axis)
        if len(axis_attr_coords) != 1:
            # ambiguous: more than one variable with same axis attribute value
            continue

        axis_attr_coord = axis_attr_coords[0]
        if len(dst[axis_attr_coord].dims) != 1:
            # not an axis coordinate
            continue

        axis_coord_dim = dst[axis_attr_coord].dims[0]
        cf_dims = dict(zip(*np.unique(
            list(chain.from_iterable(dst[_].dims for _ in dst.coords)),
            return_counts=True)))
        if cf_dims[axis_coord_dim] == 1:
            # unique coordinate variable depending on this axis
            cf_axis_coords[axis] = axis_attr_coord
            cf_axis_dims[axis] = axis_coord_dim
        elif axis_coord_dim == axis_attr_coord:
            # coordinate and dimension share same name
            cf_axis_coords[axis] = axis_attr_coord
            cf_axis_dims[axis] = axis_coord_dim

    return cf_axis_coords, cf_axis_dims


def _guess_cf_axes(dst: xr.Dataset) -> T.Tuple[
        T.Dict[str, T.Hashable], T.Dict[str, str], T.List[T.Hashable]]:
    """Guess the CF axis dimensions in a dataset and return a dictionary
    where keys are the found CF axes and values the corresponding
    coordinate names in the dataset.
    """
    # check coordinates have been guessed already
    assert CB_COORDS in dst.encoding

    # dimensions that are CF standard axes (X, Y, Z, T)
    # key = standard axis, value = dimension name in dataset
    cf_axis_dims: T.Dict[str, T.Hashable] = {}

    # coordinates that are considered as axes as they depend on an axis
    # dimension not shared without other coordinates or are unidimensional
    cf_axis_coords: T.Dict[str, str] = {}

    # special axis corresponding to a feature instance in a discrete collection
    cf_instance_dims: T.Set[T.Hashable] = set()

    # get the dimension axes used by the CF coordinates and their
    # occurrences
    cf_dims = dict(zip(*np.unique(
        list(chain.from_iterable(
            dst[_].dims for _ in dst.encoding.get(CB_COORDS).values()
        )),
        return_counts=True)))

    # get axis coordinates with explicit axis attribute
    _cf_axis_coords, _cf_axis_dims = _guess_explicit_axis_coordinates(dst)
    cf_axis_coords.update(_cf_axis_coords)
    cf_axis_dims.update(_cf_axis_dims)

    # identify the axes unique to some coordinate = axis coordinates
    for cf_coord in cf.CF_COORDS:
        if cf_coord not in dst.encoding.get(CB_COORDS):
            # coordinate not existing or not identified in the dataset
            continue
        coord = dst.encoding.get(CB_COORDS)[cf_coord]

        # dimensionless coordinate must be an axis
        if len(dst[coord].dims) == 0:
            _set_axis(dst, coord, cf.GEOCOORD_AXIS[cf_coord])
            #cf_axis_coords[cf.GEOCOORD_AXIS[cf_coord]] = coord
            continue

        # latitude(dim_0), longitude(dim_1) => independant axes for lat , lon
        lat_dims = set(dst[dst.encoding.get(CB_COORDS)['latitude']].dims)
        lon_dims = set(dst[dst.encoding.get(CB_COORDS)['longitude']].dims)

        if cf_coord in ['latitude', 'longitude'] and \
                lat_dims.intersection(lon_dims) == set():
            cf_axis_coords[cf.GEOCOORD_AXIS[cf_coord]] = coord
            cf_axis_dims[cf.GEOCOORD_AXIS[cf_coord]] = dst[coord].dims[0]
            _set_axis(dst, coord, cf.GEOCOORD_AXIS[cf_coord])
            continue

        if len(dst[coord].dims) == 1:
            # coordinate has one unique axis
            udim = dst[coord].dims[0]

            # latitude(dim_0), longitude(dim_1)
            if cf_dims[udim] == 1:
                # this axis is only used by this coordinate => it is an
                # axis coordinate
                cf_axis_coords[cf.GEOCOORD_AXIS[cf_coord]] = coord
                cf_axis_dims[cf.GEOCOORD_AXIS[cf_coord]] = udim
                _set_axis(dst, coord, cf.GEOCOORD_AXIS[cf_coord])
                # @TODO Dirty workaround for TimeSeriesProfile. We need
                #  better identification/separation of instance and element
                #  variables
                if (len(lon_dims) == len(lat_dims) == 0 and
                        cf_coord != 'vertical' and
                        'Z' in cf_axis_coords):
                    cf_instance_dims = cf_instance_dims.union({udim})

            elif (cf_dims[udim] == len(dst.encoding.get(CB_COORDS)) or
                  ('vertical' in dst.encoding.get(CB_COORDS) and
                   cf_dims[udim] == len(dst.encoding.get(CB_COORDS))-1)):
                # all coords depend on the same dimension - if not time it
                # is guessed as an instance dimension
                if udim != 'time':
                    cf_instance_dims = {udim}
                elif cf.GEOCOORD_AXIS[cf_coord] == 'T':
                    cf_axis_dims[cf.GEOCOORD_AXIS[cf_coord]] = udim

                # coord is a dimensionless axis coordinate
                cf_axis_coords[cf.GEOCOORD_AXIS[cf_coord]] = coord
                _set_axis(dst, coord, cf.GEOCOORD_AXIS[cf_coord])

        elif len(dst[coord].dims) > 1:
            # the coordinate has multiple dimensions => mix of instance
            # and/or CF geospatial dimensions
            udim = [_ for _ in dst[coord].dims if cf_dims[_] == 1]
            if len(udim) == 1:
                # only one is unique to this coordinate => must be the
                # geospatial axis
                udim = udim[0]
                cf_axis_coords[cf.GEOCOORD_AXIS[cf_coord]] = coord
                cf_axis_dims[cf.GEOCOORD_AXIS[cf_coord]] = udim
                _set_axis(dst, coord, cf.GEOCOORD_AXIS[cf_coord])

                # remaining dim(s) must be collection instance dimension(s)
                cf_instance_dims = cf_instance_dims.union(
                    set(dst[coord].dims) - {udim}
                )

    # guess axis dimensions based on name
    for dim in dst.dims:
        if dim in match.DIM_MATCHING:
            axis_dim = match.DIM_MATCHING[dim]
            if (axis_dim in cf_axis_dims
                    and dim != cf_axis_dims[axis_dim]):
                warnings.warn(
                    f'Found more than one dimension for axis {axis_dim}: '
                    f'{dim} {cf_axis_dims[axis_dim]}. Keeping '
                    f'{cf_axis_dims[axis_dim]} as {axis_dim} axis',
                    cerbere.CWarning)
            else:
                cf_axis_dims[axis_dim] = dim

    dst.encoding[CB_AXIS_DIMS] = cf_axis_dims
    dst.encoding[CB_AXIS_COORDS] = cf_axis_coords

    return cf_axis_dims, cf_axis_coords, list(cf_instance_dims),

    # # find explicit axis coordinates having a proper CF variable
    # # attribute `axis`
    # missing_axis_coords = []
    # for axis in cf.CF_AXIS:
    #     try:
    #         cf_axis_coord[axis] = DatasetAccessor._find_axis_coord(dst, axis)
    #     except cerbere.AxisError:
    #         missing_axis_coords.append(axis)
    #
    #
    # if len(missing_axis_coords) == 0:
    #     # all axes found
    #     # verify they are truly axes
    #     DatasetAccessor._verify_cf_axes(dst, geo_axes)
    #
    #     # guess instance axes (for collection of features)
    #
    #     return geo_axes
    #
    # # check if spatiotemporal coordinates are axes
    # for coord in cf.CF_REQ_GEOCOORDS:
    #     dst_coord = dst.encoding[CB_COORDS].get(coord)
    #     axis = cf.GEOCOORD_AXIS[coord]
    #     if len(dst[dst_coord].dims) == 0 and axis not in geo_axes:
    #         geo_axes[axis] = dst_coord
    #
    # return geo_axes