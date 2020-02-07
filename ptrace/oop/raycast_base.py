"""Base classes for handling rays and results of their casting onto scene
   geometry."""


from .vector import Vec3

class Ray():
    """Represents and oriented ray defined by its origin and direction."""

    origin = None
    direction = None

    def __init__(self, origin, direction):
        """Creates a ray with given origin and direction.

           Direction must be normalised."""
        self.origin = origin
        self.direction = direction

    @staticmethod
    def from_points(origin, point):
        """Creates a ray with origin at first point and directed towards second
           point."""
        return Ray(origin, (point - origin).normalised())

    def point_at(self, distance):
        """returns vector representing position of a point on the ray at given
           distance from the origin."""
        return self.origin + self.direction * distance


#pylint: disable=too-few-public-methods

class HitRecord():
    """Stores information about detected intersection of a ray with scene
       geometry."""

    distance = 0.0
    position = None
    is_inside = False
    normal = None

    def __init__(self, distance, position, is_inside=False, normal=None):
        """Initializes simple hit record object with given data."""

        self.distance = distance
        self.position = position
        self.is_inside = is_inside
        self.normal = normal if normal is not None else Vec3.versor(0)

#pylint: enable=too-few-public-methods
