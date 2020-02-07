"""Variety of general-purpose utility functions."""

import math
import numpy as np

def isiter(obj):
    """Checks whether given object is iterable."""
    return obj is not None and hasattr(obj, '__iter__')

def deg2rad(angle):
    """Converts value in degrees to radians."""
    return angle * math.pi / 180.0

def rad2deg(angle):
    """Converts value in radians to degrees."""
    return angle * 180.0 / math.pi

_COLOUR2BYTE_CONV_EXP = 1.0 / 2.2

def colour2bytes(colour):
    """Converts colour (as Vec3) to equivalent array of bytes.

       Note taht values between 0 and 1 are not scaled linearly."""
    return np.floor(np.power(np.clip(colour.data(), 0.0, 1.0), \
                             _COLOUR2BYTE_CONV_EXP) * 255.0).astype('uint8')
