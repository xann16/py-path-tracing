"""Classes for storing and creating scene contents."""

import math

from .vector import Vec3
from .raycast_base import HitRecord
from .oop_primitives import Primitive, Sphere, Triangle
from .oop_material import material_from_data

class Scene(Primitive):
    """Represents scene being rendered."""

    primitives = None
    environment_colour = None

    def __init__(self, environment_colour):
        """Creates empty scene with given environment colour."""
        self.environment_colour = environment_colour
        self.primitives = []

    def add(self, primitive):
        """Adds new geometry primitive to the scenr."""
        self.primitives.append(primitive)

    def intersect_ex(self, ray):
        """Checks whether given ray intersects with scene geometry."""
        result = {'hit_record': HitRecord(float('inf'), Vec3()), 'material': None}
        for primitive in self.primitives:
            hit = primitive.intersect_ex(ray)
            if hit and hit['hit_record'].distance < result['hit_record'].distance:
                result = hit
        if math.isinf(result['hit_record'].distance):
            return None
        return result


class SceneBuilder():
    """Constructs scene from given geometry primitives."""

    scene = None

    def __init__(self, environment_colour):
        """Initializes empty scene with given environment colour."""
        self.scene = Scene(environment_colour)

    def add_sphere(self, centre, radius, material_data):
        """Adds sphere of given dimensions and with given material to the scene.
        """
        self.scene.add(Sphere(centre, radius, material_from_data(material_data)))

    def add_triangle(self, vertices, material_data, normals=None):
        """Adds triangle with given vertices and material to the scene.
        """
        self.scene.add(Triangle(vertices, material_from_data(material_data), normals))
