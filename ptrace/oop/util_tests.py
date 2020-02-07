"""Unit tests for utility common classes."""

import unittest
import math
import numpy as np

from .vector import Vec3

from .utils import isiter, rad2deg, deg2rad, colour2bytes
from .image_output import AccumulableImage
from .scene_settings import MaterialData

class UtilsTests(unittest.TestCase):
    """Tests for functions in utils.py module."""

    def test_util_isiter(self):
        """Tests for 'isiter' function."""
        self.assertTrue(isiter([]))
        self.assertTrue(isiter({}))
        self.assertTrue(isiter(set()))
        self.assertTrue(isiter('abc'))
        self.assertFalse(isiter(1))
        self.assertFalse(isiter(1.234))
        self.assertFalse(isiter(None))

    def test_util_rad_deg_conv(self):
        """Tests for radian-degree conversion functions."""

        degs_in_rad = 57.295779513082320

        self.assertAlmostEqual(rad2deg(math.pi), 180.0)
        self.assertAlmostEqual(rad2deg(math.pi / 2), 90.0)
        self.assertAlmostEqual(rad2deg(math.pi * 2), 360.0)
        self.assertAlmostEqual(rad2deg(1), degs_in_rad)
        self.assertAlmostEqual(rad2deg(0), 0.0)

        self.assertAlmostEqual(deg2rad(180.0), math.pi)
        self.assertAlmostEqual(deg2rad(90.0), math.pi / 2)
        self.assertAlmostEqual(deg2rad(360.0), math.pi * 2)
        self.assertAlmostEqual(deg2rad(degs_in_rad), 1)
        self.assertAlmostEqual(deg2rad(0.0), 0)

        for val in np.linspace(-5, 5, 100):
            self.assertAlmostEqual(rad2deg(deg2rad(val)), val)
            self.assertAlmostEqual(deg2rad(rad2deg(val)), val)

    def test_util_c2b(self):
        """Tests 'colour2bytes' conversion function."""
        self.assertTrue(np.allclose(colour2bytes(Vec3(2, 2, 2)), \
                                    np.array([255, 255, 255], dtype='uint8')))
        self.assertTrue(np.allclose(colour2bytes(Vec3(1, 1, 1)), \
                                    np.array([255, 255, 255], dtype='uint8')))
        self.assertTrue(np.allclose(colour2bytes(Vec3(0, 0, 0)), \
                                    np.array([0, 0, 0], dtype='uint8')))
        self.assertTrue(np.allclose(colour2bytes(Vec3(-1, -1, -1)), \
                                    np.array([0, 0, 0], dtype='uint8')))


class AccumulableImageTests(unittest.TestCase):
    """Tests for AccumulableImage class."""

    def test_accimg_basic(self):
        """Tests for basic class functionalities."""
        img = AccumulableImage(12, 8)
        self.assertEqual(img.width, 12)
        self.assertEqual(img.height, 8)

        for pos in [(i, j) for i in range(12) for j in range(8)]:
            self.assertEqual(img[pos], Vec3())
            self.assertTrue(np.allclose(img.bytes_at(pos), np.array([0, 0, 0], dtype='uint8')))
            self.assertEqual(img.sample_counts[pos[0], pos[1]], 0)

    def test_accimg_addition(self):
        """Tests adding samples and whole images."""

        img = AccumulableImage(12, 8)
        img2 = AccumulableImage(12, 8)

        colour = Vec3(0.1, 0.5, 0.9)
        c_bytes = colour2bytes(colour)

        for pos in [(i, j) for i in range(12) for j in range(8)]:
            x_pos, y_pos = pos
            samples = x_pos + y_pos + 1
            img.add_samples(x_pos, y_pos, colour, samples)
            img2.add_samples(x_pos, y_pos, colour, samples)

        img2 += img

        for pos in [(i, j) for i in range(12) for j in range(8)]:
            samples = pos[0] + pos[1] + 1
            self.assertEqual(img[pos], colour)
            self.assertEqual(img2[pos], colour)
            self.assertTrue(np.allclose(img.bytes_at(pos), c_bytes))
            self.assertTrue(np.allclose(img2.bytes_at(pos), c_bytes))
            self.assertEqual(img.sample_counts[pos[0], pos[1]], samples)
            self.assertEqual(img2.sample_counts[pos[0], pos[1]], samples * 2)


class MaterialDataTests(unittest.TestCase):
    """Tests for MaterialData class."""

    def test_mat_basic(self):
        """Tests for basic class functionalities."""
        self.assertTrue(MaterialData.make_diffuse(Vec3()), MaterialData.make_light(Vec3()))
