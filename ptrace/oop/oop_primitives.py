"""Classes representing basic geometry primitives used in scenes."""

import math

from .raycast_base import HitRecord

_EPS = 0.0000001


class Primitive():
    """Base class for geometry primitives."""

    material = None

    #pylint: disable=no-self-use

    def intersect(self, _):
        """Checks whether given ray intersects with the primitive."""
        return None

    #pylint: enable=no-self-use
    #pylint: disable=assignment-from-none

    def intersect_ex(self, ray):
        """Checks whether given ray intersects with the primitive (returns extra
           information on primitive's material)."""
        hit = self.intersect(ray)
        if not hit:
            return None
        return {'hit_record': hit, 'material': self.material}

    #pylint: enable=assignment-from-none


class Sphere(Primitive):
    """Class representing geometry of a sphere."""

    centre = None
    radius = 0.0

    def __init__(self, centre, radius, material=None):
        """Creates a sphere with given centre point and radius."""
        assert radius >= 0.0
        self.centre = centre
        self.radius = radius
        self.material = material

    def is_inside(self, point):
        """Checks whether point lies within the sphere."""
        return abs(point - self.centre) <= self.radius

    def intersect(self, ray):
        """Checks whether given ray intersects with the sphere.

           In practice boils down to solving equation:
             t^2*d.d + 2*t*(o-p).d + (o-p).(o-p)-R^2 = 0."""
        orig = self.centre - ray.origin
        r_sqr = self.radius ** 2
        b_coeff = orig.dot(ray.direction)
        discr = b_coeff ** 2 - orig.sqr_length() + r_sqr
        if discr < 0.0:
            return None

        discr = math.sqrt(discr)
        t_neg = b_coeff - discr
        t_pos = b_coeff + discr
        if t_neg < _EPS and t_pos < _EPS:
            return None

        t_val = t_neg if t_neg > _EPS else t_pos
        hit_pos = ray.point_at(t_val)
        hit_norm = (hit_pos - self.centre).normalised()
        hit_inside = hit_norm.dot(ray.direction) > 0.0
        if hit_inside:
            hit_norm = -hit_norm
        return HitRecord(t_val, hit_pos, hit_inside, hit_norm)

class Triangle(Primitive):
    """Class representing geometry of a triangle."""

    vertices = None
    normals = None

    def __init__(self, vertices, material=None, normals=None):
        """Creates triangle with vertices at given points and their respective
           normal vectors."""
        self.vertices = vertices
        self.material = material
        self.normals = normals if normals is not None \
             else [self.face_normal(), self.face_normal(), self.face_normal()]

    def face_u(self):
        """Returns triangle face coordinate u vector."""
        return self.vertices[1] - self.vertices[0]

    def face_v(self):
        """Returns triangle face coordinate v vector."""
        return self.vertices[2] - self.vertices[0]

    def face_normal(self):
        """Returns normal vector to triangle face."""
        return self.face_u().cross(self.face_v()).normalised()

    def intersect(self, ray):
        """Checks whether given ray intersects with the triangle."""

        p_vec = ray.direction.cross(self.face_v())
        det = self.face_u().dot(p_vec)

        # ray || triangle
        if abs(det) < _EPS:
            return None

        is_backface = det < _EPS
        t_vec = ray.origin - self.vertices[0]
        u_pos = t_vec.dot(p_vec) / det

        q_vec = t_vec.cross(self.face_u())
        v_pos = ray.direction.dot(q_vec) / det

        # ray misses triangle
        if u_pos < 0.0 or u_pos > 1.0 or v_pos < 0.0 or u_pos + v_pos > 1.0:
            return None

        # edge case
        t_val = self.face_v().dot(q_vec) / det
        if t_val < _EPS:
            return None

        delta_u_norm = self.normals[1] - self.normals[0]
        delta_v_norm = self.normals[2] - self.normals[0]
        hit_norm = (delta_u_norm * u_pos + delta_v_norm * v_pos + self.normals[0]).normalised()
        if is_backface:
            hit_norm = -hit_norm

        return HitRecord(t_val, ray.point_at(t_val), is_backface, hit_norm)
