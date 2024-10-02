# -*- coding: utf-8 -*-

"""
cerbere.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Cerbere exceptions.
"""


class AxisError(Exception):
    """Exception class for CF axis coordinates management"""
    pass


class BadAxisError(AxisError):
    pass


class MissingAxisError(AxisError):
    pass


class CoordinateError(Exception):
    """Exception class for CF spatial and temporal coordinates management"""
    pass


class FeatureTypeError(Exception):
    pass


# warnings
class CWarning(UserWarning):
    """Cerbere warning class"""
    pass
