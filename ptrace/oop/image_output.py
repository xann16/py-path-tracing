"""Classes handling output data of rendered image that is being accumulated
   throughout rendering process."""

import numpy as np

from .utils import colour2bytes
from .vector import Vec3


class AccumulableImage():
    """Represents 2D RGB image whose pixel values can be accumulated during
       rendering process."""

    width = None
    height = None
    image = None
    sample_counts = None

    def __init__(self, width, height):
        """Initializes empty accumulable image of given dimensions.

            Optionally, may be initialized with iterable sample data source."""
        self.width = width
        self.height = height
        self.image = np.zeros((3, width, height), dtype='double')
        self.sample_counts = np.zeros((width, height), dtype='int')

    def add_samples(self, x_pos, y_pos, colour, sample_count):
        """Adds given number of samples with specified colour (as Vec3) to pixel
           at given position."""
        self.image[:, x_pos, y_pos] += colour.data() * sample_count
        self.sample_counts[x_pos, y_pos] += sample_count

    def __getitem__(self, pos):
        """Returns colour (as Vec3) of a pixel at given position adjusted by the
           number of samples accumulated."""
        divisor = max(1, self.sample_counts[pos])
        return Vec3.from_array(self.image[:, pos[0], pos[1]] / divisor)

    def bytes_at(self, pos):
        """Returns length 3 byte array representing colour of a pixel at given
           position."""
        return colour2bytes(self[pos])

    def __iadd__(self, other):
        """Adds all respective colour values and sample counts from another
           accumulable image to the current one."""
        assert self.width == other.width and self.height == other.height
        self.image += other.image
        self.sample_counts += other.sample_counts
        return self

    def total_sample_count(self):
        """Returns total number of samples accumulated."""
        return np.sum(self.sample_counts)
