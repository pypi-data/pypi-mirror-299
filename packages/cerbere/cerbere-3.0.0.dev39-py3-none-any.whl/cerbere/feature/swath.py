# -*- coding: utf-8 -*-
"""
Class for the swath feature
"""
from __future__ import absolute_import, division, print_function

from cerbere.feature.feature import Feature

__all__ = ['Swath']


class Swath(Feature):
    """
    Feature class for representing a swath, a two-dimensional irregular grid
    along the satellite track.
    """
    _feature_geodimnames = 'row', 'cell',

    def __init__(self, *args, **kwargs):
        # create feature
        super(Swath, self).__init__(
            *args,
            **kwargs
        )

    def get_geocoord_dimnames(self, fieldname, shape=None):
        if fieldname == 'depth':
            return 'depth',
        else:
            return 'row', 'cell',



#     def extract_subset(
#             self, boundaries=None, slices=None, fields=None, padding=False,
#             prefix=None):
#         """Extract a subset feature from the swath.
#
#         The created subset is a new Swath object without any reference to
#         the source.
#
#         Args:
#             boundaries (tuple): area of the subset to extract, defined as
#                 llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat.
#
#             slices (dict): indices for /time/ dimension of the subset to
#                 extract from the source data. If None, the complete feature
#                 is extracted.
#
#             fields (list): list of field names to extract. If None, all fields
#                 are extracted.
#
#             padding (bool): Passed to extract_field method to ensure padding
#                 with _FillValues for points outside of the bounds of the this
#                 feature (used only in conjuncture with slices.
#
#             prefix (str): add a prefix string to the field names of the
#                 extracted subset.
#         """
#         if boundaries and slices:
#             raise ValueError("Boundaries and slices can not be both provided.")
#         if boundaries:
#             # get corresponding slices
#             raise ValueError("Not yet implemented")
#         elif slices:
#             if len(slices) != 2:
#                 raise ValueError(
#                     "slices for the two spatial dimensions of "
#                     "the swath must be provided"
#                 )
#
#         # fields to extract
#         extr_fields = OrderedDict([])
#         for f in GEOCOORDINATES:
#             if f in self.get_geolocation_fields():
#                 extr_fields[f] = self.extract_field(
#                     f, slices=slices, padding=padding
#                 )
#         sub_swath = Swath(
#             latitudes=self.extract_field(
#                 'lat', slices=slices, padding=padding),
#             longitudes=self.extract_field(
#                 'lon', slices=slices, padding=padding
#             ),
#             times=self.extract_field('time', slices=slices, padding=padding),
#             depths=self.extract_field('z', slices=slices, padding=padding),
#             attrs=self.xrdataset.attrs
#         )
#
#         if fields is None:
#             fields = self.get_fieldnames()
#         elif not isinstance(fields, list):
#             raise TypeError("fields must be a list")
#         for field in fields:
#             if field not in self.get_fieldnames():
#                 raise ValueError("Field %s not existing" % field)
#             sub_swath.add_field(
#                 self.extract_field(field,
#                                    slices=slices,
#                                    padding=padding,
#                                    prefix=prefix)
#             )
#         return sub_swath

    # def get_spatial_resolution(self):
    #     """Return the spatial resolution of the feature"""
    #     if self.spatial_resolution is None:
    #         i = self.get_geolocation_dimsizes()['cell'] / 2
    #         j = self.get_geolocation_dimsizes()['row'] / 2
    #         res = Point.get_distance(
    #             Point(self.get_lon(
    #                 slices={'row': slice(j, j + 1, 1),
    #                         'cell': slice(i, i + 1, 1)}
    #             ),
    #                 self.get_lat(
    #                 slices={'row': slice(j, j + 1, 1),
    #                         'cell': slice(i, i + 1, 1)}
    #             )),
    #             Point(self.get_lon(
    #                 {'row': slice(j + 1, j + 2, 1),
    #                  'cell': slice(i + 1, i + 2, 1)}
    #             ),
    #                 self.get_lat(
    #                 {'row': slice(j + 1, j + 2, 1),
    #                  'cell': slice(i + 1, i + 2, 1)}
    #             ))
    #         ).ravel()[0] / numpy.sqrt(2)
    #         return res
