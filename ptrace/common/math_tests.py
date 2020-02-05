"""Unit tests for math-oriented common classes."""


import unittest
import math
import numpy as np

from .vector import Vec3, OrthonormalBasis
from .raycast_base import Ray
from .camera import Camera


class Vec3Tests(unittest.TestCase):
    """Test for Vec3 class."""

    def test_vec3_basic(self):
        """Basic creation, access and manipulation of vector components."""
        zero = Vec3()
        vvv = Vec3(1, 2, 3)
        x_arr = np.array([.1, .2, .3], dtype='double')
        xxx = Vec3.from_array(x_arr)

        ones = Vec3.full(1.0)
        i_hat = Vec3.versor(0)

        self.assertEqual(zero[0], 0.0)
        self.assertEqual(zero[1], 0.0)
        self.assertEqual(zero[2], 0.0)

        self.assertEqual(vvv[0], 1.0)
        self.assertEqual(vvv[1], 2.0)
        self.assertEqual(vvv[2], 3.0)

        vvv[2] = 10
        self.assertEqual(vvv[2], 10.0)

        self.assertEqual(str(vvv), '[ 1.  2. 10.]')

        self.assertEqual(xxx[0], .1)
        self.assertEqual(xxx[1], .2)
        self.assertEqual(xxx[2], .3)

        self.assertEqual(ones[0], 1)
        self.assertEqual(ones[1], 1)
        self.assertEqual(ones[2], 1)

        self.assertEqual(i_hat[0], 1)
        self.assertEqual(i_hat[1], 0)
        self.assertEqual(i_hat[2], 0)

        is_v_eq = np.allclose(vvv.data(), np.array([1, 2, 10]))
        self.assertEqual(is_v_eq, True)
        is_x_eq = np.allclose(xxx.data(), x_arr)
        self.assertEqual(is_x_eq, True)

        self.assertEqual(vvv.copy(), vvv)

    def test_vec3_arithmetic_and_comparisons(self):
        """Testing methods and operators used for arithmentic and comparisons.
           """
        xxx = Vec3(1, 2, 3)
        yyy = Vec3(1, 2, 3)
        zzz = Vec3(1, 0, -1)

        self.assertEqual(xxx == yyy, True)
        self.assertEqual(xxx != yyy, False)
        self.assertEqual(xxx != zzz, True)
        self.assertEqual(xxx == zzz, False)
        self.assertEqual(yyy != zzz, True)
        self.assertEqual(yyy == zzz, False)

        yyy += zzz
        self.assertEqual(yyy, Vec3.full(2))
        self.assertEqual(yyy + xxx, Vec3(3, 4, 5))

        yyy -= zzz
        self.assertEqual(yyy, xxx)
        self.assertEqual(yyy - xxx, Vec3())

        self.assertEqual(+xxx, xxx)
        self.assertEqual(-xxx, Vec3(-1, -2, -3))

        yyy *= -1
        self.assertEqual(yyy, -xxx)
        self.assertEqual(yyy * -1.0, xxx)

        zzz /= 2
        self.assertEqual(zzz, Vec3(.5, 0, -.5))
        self.assertEqual(zzz / 2, Vec3(.25, 0, -.25))

        vvv = Vec3(3, 1, -2)
        vvv *= Vec3(2, .5, -1)
        self.assertEqual(vvv, Vec3(6, .5, 2))
        self.assertEqual(vvv * Vec3.full(2), Vec3(12, 1, 4))

        www = Vec3.full(10)
        www /= Vec3(10, 5, 2)
        self.assertEqual(www, Vec3(1, 2, 5))
        self.assertEqual(www / 2, Vec3(.5, 1, 2.5))

        self.assertAlmostEqual(www.dot(Vec3()), 0)
        self.assertAlmostEqual(Vec3(1, 2, 4).dot(Vec3(1, -2, 1)), 1)

        self.assertEqual(Vec3.versor(0).cross(Vec3.versor(1)), Vec3.versor(2))
        self.assertEqual(Vec3.versor(1).cross(Vec3.versor(2)), Vec3.versor(0))
        self.assertEqual(Vec3.versor(2).cross(Vec3.versor(0)), Vec3.versor(1))
        self.assertEqual(Vec3.versor(1).cross(Vec3.versor(0)), -Vec3.versor(2))
        self.assertEqual(Vec3.versor(1).cross(Vec3.versor(1)), Vec3())

        self.assertEqual(Vec3(1, 2, 3).isclose(Vec3(1, 2, 3)), True)
        self.assertEqual(Vec3(1, 2, 3).isclose(Vec3(1, 2.0001, 3), 0.1), True)


    def test_vec3_normalization(self):
        """Testing length calculations and normalisation."""
        self.assertAlmostEqual(Vec3().sqr_length(), 0.0)
        self.assertAlmostEqual(Vec3().length(), 0.0)

        self.assertAlmostEqual(Vec3.versor(0).sqr_length(), 1.0)
        self.assertAlmostEqual(Vec3.versor(1).length(), 1.0)
        self.assertAlmostEqual(abs(Vec3.versor(2)), 1.0)

        self.assertEqual(Vec3.versor(0).normalised(), Vec3.versor(0))
        self.assertEqual(Vec3.versor(1).normalised(), Vec3.versor(1))
        self.assertEqual(Vec3.versor(2).normalised(), Vec3.versor(2))

        sqrt3 = math.sqrt(3)
        v_sqrt3_inv = Vec3.full(1. / sqrt3)
        self.assertAlmostEqual(Vec3.full(1).sqr_length(), 3)
        self.assertAlmostEqual(Vec3.full(1).length(), sqrt3)
        self.assertEqual(Vec3.full(1).normalised(), v_sqrt3_inv)


    def test_vec3_reflection(self):
        """Testing reflection with respect to given normal vector."""
        nnn = Vec3.versor(2)

        self.assertEqual(nnn.reflect(Vec3.versor(0)), Vec3.versor(0))
        self.assertEqual(nnn.reflect(Vec3.versor(2)), -Vec3.versor(2))

        diag = Vec3(1, 1, 1).normalised()
        diag_refl = diag.copy()
        diag_refl[2] = -diag_refl[2]

        self.assertEqual(nnn.reflect(diag), diag_refl)


class OrthonormalBasisTests(unittest.TestCase):
    """Tests for OrthonormalBasis class."""

    def test_onb_basic(self):
        """Basic test reconstructing natural ONB."""
        nat = OrthonormalBasis(Vec3.versor(0), Vec3.versor(1), Vec3.versor(2))
        nat_alt = OrthonormalBasis.from_two('xy', Vec3.versor(0), Vec3.versor(1))
        vvv = Vec3(1, 2, 3)

        self.assertEqual(nat.transform(vvv), vvv)
        self.assertEqual(nat_alt.transform(vvv), vvv)

    def test_onb_factories(self):
        """Testing factory methods for creating ONBs from one or two vectors."""
        onb1 = OrthonormalBasis.from_two('xy', Vec3(1, 2, 4).normalised(),\
                                               Vec3(0, 0, -7).normalised())

        self.assertAlmostEqual(abs(onb1.x_axis), 1.0)
        self.assertAlmostEqual(abs(onb1.y_axis), 1.0)
        self.assertAlmostEqual(abs(onb1.z_axis), 1.0)
        self.assertAlmostEqual(onb1.x_axis.dot(onb1.y_axis), 0.0)
        self.assertAlmostEqual(onb1.x_axis.dot(onb1.z_axis), 0.0)
        self.assertAlmostEqual(onb1.y_axis.dot(onb1.z_axis), 0.0)

        onb2 = OrthonormalBasis.from_two('zx', Vec3(-1, -1, -1).normalised(),\
                                               Vec3(1, 1, -1).normalised())

        self.assertAlmostEqual(abs(onb2.x_axis), 1.0)
        self.assertAlmostEqual(abs(onb2.y_axis), 1.0)
        self.assertAlmostEqual(abs(onb2.z_axis), 1.0)
        self.assertAlmostEqual(onb2.x_axis.dot(onb2.y_axis), 0.0)
        self.assertAlmostEqual(onb2.x_axis.dot(onb2.z_axis), 0.0)
        self.assertAlmostEqual(onb2.y_axis.dot(onb2.z_axis), 0.0)

        onb3 = OrthonormalBasis.from_z_axis(Vec3.versor(0))

        self.assertAlmostEqual(abs(onb3.x_axis), 1.0)
        self.assertAlmostEqual(abs(onb3.y_axis), 1.0)
        self.assertAlmostEqual(abs(onb3.z_axis), 1.0)
        self.assertAlmostEqual(onb3.x_axis.dot(onb3.y_axis), 0.0)
        self.assertAlmostEqual(onb3.x_axis.dot(onb3.z_axis), 0.0)
        self.assertAlmostEqual(onb3.y_axis.dot(onb3.z_axis), 0.0)


class RayTests(unittest.TestCase):
    """Tests for Ray class."""

    def test_ray_basic(self):
        """Basic tests chcecking ray creation and probing their points."""
        ox_axis = Ray(Vec3(), Vec3.versor(0))
        self.assertEqual(ox_axis.point_at(4), Vec3(4, 0, 0))

        direction = Vec3(1, -1, 0).normalised()
        ray1 = Ray(Vec3(0, 2, 0), direction)
        ray2 = Ray.from_points(Vec3(0, 2, 0), Vec3(2, 0, 0))

        self.assertEqual(ray1.direction, direction)
        self.assertEqual(ray2.direction, direction)

        for i in range(10):
            self.assertEqual(ray1.point_at(i), ray2.point_at(i))

        self.assertEqual(ray1.point_at(0), ray1.origin)
        self.assertEqual(ray2.point_at(0), ray2.origin)


class CameraTests(unittest.TestCase):
    """Tests for Camera class."""

    def test_cam_basic(self):
        """Basic test checking if camera casts rays in correct direction."""
        cam = Camera(Vec3(), Vec3.versor(0), Vec3.versor(2), 10, 10, 120)
        cam.set_focus(Vec3.versor(0), 1.0)

        for px_x in range(10):
            for px_y in range(10):
                ray = cam.get_ray(px_x, px_y)
                self.assertGreaterEqual(ray.direction.dot(Vec3.versor(0)), 0.0)


if __name__ == '__main__':
    unittest.main()
