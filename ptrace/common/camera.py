"""Abstract camera for rendering scenes."""

import math
import random

from .vector import OrthonormalBasis
from .raycast_base import Ray

#pylint: disable=too-many-arguments
#pylint: disable=too-many-instance-attributes


class Camera():
    """Represents abstract camera object that serves as a perspective from
       which given scene is rendered."""

    position = None
    basis = None
    aspect_ratio = 1.0
    camera_plane_dist = 0.0
    reciprocal_height = 0.0
    reciprocal_width = 0.0
    aperture_radius = 0.0
    focal_distance = 0.0

    def __init__(self, eye, look_at, up, width, height, vertical_fov):
        """Creates new camera object using standard positioning vectors (i.e.
           eye position, point looking at, and up direction - normalised), as
           well as resulting image dimensions and verical field of view angle
           (given in degrees).
           """
        self.position = eye
        self.basis = OrthonormalBasis.from_two('zy',
                                               (look_at - eye).normalised(), up)
        self.aspect_ratio = float(width) / float(height)
        self.camera_plane_dist = 1.0 / math.tan(vertical_fov * math.pi / 360.0)
        self.reciprocal_height = 1.0 / float(height)
        self.reciprocal_width = 1.0 / float(width)

    def set_focus(self, focal_pt, aperture_radius):
        """Sets focus parameters for given camera."""
        self.focal_distance = abs(focal_pt - self.position)
        self.aperture_radius = aperture_radius

    def get_ray(self, px_x, px_y):
        """Casts a random ray from camera that corresponds to the center of an
           output pixel with indices 'px_x' and 'px_y'."""
        xxx = (float(px_x) + random.random()) * self.reciprocal_width
        yyy = (float(px_y) + random.random()) * self.reciprocal_height
        return self._ray_from_unit(2.0 * xxx - 1.0, 2.0 * yyy - 1.0)

    def _ray_from_unit(self, x_pos, y_pos):
        """Casts new ray from within camera's field of view acording to uniform
           units."""
        xxx = self.basis.x_axis * -x_pos * self.aspect_ratio
        yyy = self.basis.y_axis * -y_pos
        zzz = self.basis.z_axis * self.camera_plane_dist
        direction = (xxx + yyy + zzz).normalised()
        if self.aperture_radius == 0:
            return Ray(self.position, direction)

        focal_pt = self.position + direction * self.focal_distance

        angle = random.uniform(0, 2.0 * math.pi)
        radius = random.uniform(0, self.aperture_radius)
        origin = self.position + \
                 self.basis.x_axis * math.cos(angle) * radius + \
                 self.basis.y_axis * math.sin(angle) * radius

        return Ray.from_points(origin, focal_pt)

#pylint: enable=too-many-arguments
#pylint: enable=too-many-instance-attributes
