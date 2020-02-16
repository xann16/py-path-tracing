"""Variety of general-purpose utility functions."""

import math
import json
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

def load_params(filename):
    """Loads rendering parameters from json file."""
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        result = json.load(jsonfile)

    assert 'width' in result and isinstance(result['width'], int)
    assert 'height' in result and isinstance(result['height'], int)
    assert 'samples_per_pixel' in result and isinstance(result['samples_per_pixel'], int)
    assert 'max_cpus' in result and isinstance(result['max_cpus'], int)
    assert 'max_depth' in result and isinstance(result['max_depth'], int)
    assert 'first_bounce_u_samples' in result and isinstance(result['first_bounce_u_samples'], int)
    assert 'first_bounce_v_samples' in result and isinstance(result['first_bounce_v_samples'], int)
    assert 'preview' in result and isinstance(result['preview'], bool)

    return result
