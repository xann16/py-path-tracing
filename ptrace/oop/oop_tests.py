"""Unit tests for oop classes."""

import unittest

from .vector import Vec3
from .scene_settings import MaterialData
from .raycast_base import Ray

from .oop_material import MatteMaterial, ShinyMaterial, material_from_data
from .oop_primitives import Sphere, Triangle


class MaterialTests(unittest.TestCase):
    """Tests for Material class and its derived classes."""

    def test_mat_basic(self):
        """Tests for bacic functionalities of MAterial."""
        self.assertTrue(isinstance(material_from_data( \
            MaterialData.make_reflective(Vec3(), 0.5, 90)), ShinyMaterial))
        self.assertTrue(isinstance(material_from_data( \
            MaterialData.make_diffuse(Vec3())), MatteMaterial))

class SphereTests(unittest.TestCase):
    """Tests for Sphere class."""

    def test_sph_basic(self):
        """Tests basic sphere creation."""
        sph = Sphere(Vec3(10, 20, 30), 15)
        self.assertEqual(sph.centre, Vec3(10, 20, 30))
        self.assertAlmostEqual(sph.radius, 15)

    def test_sph_intersect_outside(self):
        """Sphere intersection test (w/outside ray)."""
        sph = Sphere(Vec3(0, 0, 30), 10)
        hit = sph.intersect(Ray.from_points(Vec3(), Vec3(0, 0, 2)))
        self.assertTrue(hit)

        self.assertAlmostEqual(hit.distance, 20)
        self.assertEqual(hit.position, Vec3(0, 0, 20))
        self.assertEqual(hit.normal, Vec3(0, 0, -1))
        self.assertFalse(hit.is_inside)

    def test_sph_intersect_inside(self):
        """Sphere intersection test (w/outside ray)."""
        sph = Sphere(Vec3(0, 0, 30), 10)
        hit = sph.intersect(Ray.from_points(Vec3(0, 0, 30), Vec3(0, 0, 2)))
        self.assertTrue(hit)

        self.assertAlmostEqual(hit.distance, 10)
        self.assertEqual(hit.position, Vec3(0, 0, 20))
        self.assertEqual(hit.normal, Vec3(0, 0, 1))
        self.assertTrue(hit.is_inside)

    def test_sph_intersect_miss(self):
        """Sphere intersection test (w/outside ray)."""
        sph = Sphere(Vec3(10, 20, 30), 15)
        self.assertTrue(sph.intersect(Ray.from_points(Vec3(), Vec3(0, 1, 0))) is None)
        self.assertTrue(sph.intersect(Ray.from_points(Vec3(), Vec3(-10, -20, -30))) is None)


class TriangleTests(unittest.TestCase):
    """Tests for Triangle class."""

    def test_tri_basic(self):
        """Tests basic triangle creation."""
        tri = Triangle([Vec3(), Vec3(0, 1, 0), Vec3(1, 0, 0)])
        self.assertEqual(tri.vertices[0], Vec3())
        self.assertEqual(tri.face_u(), Vec3(0, 1, 0))
        self.assertEqual(tri.face_v(), Vec3(1, 0, 0))
        self.assertEqual(tri.normals[1], Vec3(0, 0, -1))

    def test_tri_intersect_cw(self):
        """Triangle intersection test (clockwise winding order)."""
        tri = Triangle([Vec3(0, 0, 3), Vec3(0, 1, 3), Vec3(1, 1, 3)])

        self.assertTrue(tri.intersect(Ray.from_points(Vec3(), Vec3(0, 1, 0))) is None)
        self.assertTrue(tri.intersect(Ray.from_points(Vec3(), Vec3(0, 0, -1))) is None)

        hit = tri.intersect(Ray.from_points(Vec3(), Vec3(0, 0, 1)))

        self.assertTrue(hit)

        self.assertAlmostEqual(hit.distance, 3)
        self.assertEqual(hit.position, Vec3(0, 0, 3))
        self.assertEqual(hit.normal, Vec3(0, 0, -1))

    def test_tri_intersect_ccw(self):
        """Triangle intersection test (counter-clockwise winding order)."""
        tri = Triangle([Vec3(0, 0, 3), Vec3(1, 1, 3), Vec3(0, 1, 3)])

        self.assertTrue(tri.intersect(Ray.from_points(Vec3(), Vec3(0, 1, 0))) is None)
        self.assertTrue(tri.intersect(Ray.from_points(Vec3(), Vec3(0, 0, -1))) is None)

        hit = tri.intersect(Ray.from_points(Vec3(), Vec3(0, 0, 1)))
        self.assertTrue(hit)

        self.assertAlmostEqual(hit.distance, 3)
        self.assertEqual(hit.position, Vec3(0, 0, 3))
        self.assertEqual(hit.normal, Vec3(0, 0, -1))
