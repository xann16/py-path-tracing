"""Basic vector wrapper class, representation of orthonormal basis, and
   functions for sampling direction vectors from cone and hemisphere."""


import math
import numpy as np

class Vec3():
    """Represents basic 3D vector of doubles."""

    _arr = None

    def __init__(self, xxx=0.0, yyy=0.0, zzz=0.0, arr=None):
        """Initializes 3D vector with given values (zeros by default)
           or length 3 numpy array of doubles."""
        if arr is not None:
            assert arr.shape == (3,) and arr.dtype == 'double'
            self._arr = arr
        else:
            self._arr = np.array([xxx, yyy, zzz], dtype='double')

    def copy(self):
        """Creates a copy of a 3D Vector."""
        return Vec3.from_array(self._arr.copy())

    @staticmethod
    def from_array(nparr):
        """Factory method creating 3D Vector from length 3 nparray of doubles."""
        return Vec3(arr=nparr)

    @staticmethod
    def zero():
        """Factory method for 3D zero vector."""
        return Vec3()

    @staticmethod
    def full(val):
        """Factory method for 3D vector filled with given value."""
        return Vec3(val, val, val)

    @staticmethod
    def versor(index):
        """Factory method for 3D versor with respect to given axis."""
        assert 0 <= index < 3
        res = Vec3()
        res[index] = 1.0
        return res

    def __str__(self):
        """Represents given 3D vector as string."""
        return str(self._arr)

    def __getitem__(self, index):
        """Gets n-th component of 3D vector."""
        assert 0 <= index < 3
        return self._arr[index]

    def __setitem__(self, index, val):
        """Sets n-th component of 3D vector to given value."""
        assert 0 <= index < 3
        self._arr[index] = val

    def data(self):
        """Returns underlying numpy array representing 3D vector."""
        return self._arr

    def __pos__(self):
        """Unary plus operator (identity)."""
        return self

    #pylint: disable=invalid-unary-operand-type
    # see: https://github.com/PyCQA/pylint/issues/2436

    def __neg__(self):
        """Vector negation."""
        return Vec3.from_array(-self._arr)

    #pylint: enable=invalid-unary-operand-type

    def __add__(self, other):
        """Vector addition."""
        return Vec3.from_array(self._arr + other._arr)

    def __iadd__(self, other):
        """Vector addition (with assignment)."""
        self._arr += other._arr
        return self

    def __sub__(self, other):
        """Vector subtraction."""
        return Vec3.from_array(self._arr - other._arr)

    def __isub__(self, other):
        """Vector subtraction (with assignment)."""
        self._arr -= other._arr
        return self

    def __mul__(self, other):
        """Vector scalar or component-wise multiplication."""
        if isinstance(other, Vec3):
            return Vec3.from_array(self._arr * other._arr)
        return Vec3.from_array(self._arr * other)

    def __imul__(self, other):
        """Vector scalar or component-wise multiplication (with assignment)."""
        if isinstance(other, Vec3):
            self._arr *= other._arr
        else:
            self._arr *= other
        return self

    def __truediv__(self, other):
        """Vector scalar or component-wise division."""
        if isinstance(other, Vec3):
            return Vec3.from_array(self._arr / other.data())
        return Vec3.from_array(self._arr / other)

    def __itruediv__(self, other):
        """Vector scalar or component-wise division (with assignment)."""
        if isinstance(other, Vec3):
            self._arr /= other._arr
        else:
            self._arr /= other
        return self

    def __eq__(self, other):
        """Checks equality of two 3D Vectors (with strict epsilon)."""
        return np.allclose(self._arr, other.data())

    def __ne__(self, other):
        """Checks inequality of two 3D Vectors (with strict epsilon)."""
        return not self == other

    def isclose(self, other, epsilon=0.0001):
        """Determines whether two 3D vectors are within epsilon distance to each
           other."""
        return (self - other).sqr_length() < epsilon * 2

    def dot(self, other):
        """Dot product of two 3D vectors."""
        return np.dot(self._arr, other.data())

    def cross(self, other):
        """Cross product of two 3D vectors."""
        return Vec3.from_array(np.cross(self._arr, other.data()))

    def sqr_length(self):
        """Squared length of a 3D Vector."""
        return self.dot(self)

    def length(self):
        """Length of a 3D Vector."""
        return math.sqrt(self.sqr_length())

    def __abs__(self):
        """Length of a 3D Vector."""
        return self.length()

    def normalised(self):
        """Normalised version of 3D Vector."""
        return self / self.length()


    def reflect(self, incoming):
        """Calculates reflection of an incoming vector with respect to normal
           vector of a surface given in self.

           For proper results requires both self and incoming to be normalised.
           In such case its result is also guaranteed to be normalised."""
        return Vec3.from_array(incoming.data() - self._arr * 2.0 * self.dot(incoming))

    def reflectance(self, incoming, ior_from, ior_to):
        """ Calculates scalar reflectance from incoming direction with respect
            to surface normal given by self.

            For details see:
            http://graphics.stanford.edu/courses/cs148-10-summer/docs/2006--degreve--reflection_refraction.pdf"""

        ior_ratio = ior_from / ior_to
        cos_theta_i = -self.dot(incoming)
        sin_theta_sqr = (ior_ratio ** 2) * (1.0 - cos_theta_i ** 2)

        # case for total internal reflection
        if sin_theta_sqr > 1.0:
            return 1.0

        cos_theta_t = math.sqrt(1.0 - sin_theta_sqr)
        r_perpendicular = (ior_from * cos_theta_i - ior_to * cos_theta_t) / \
                          (ior_from * cos_theta_i + ior_to * cos_theta_t)
        #r_parallel = (ior_from * cos_theta_i - ior_to * cos_theta_t) /
        #             (ior_from * cos_theta_i + ior_to * cos_theta_t)
        r_parallel = (ior_to * cos_theta_i - ior_from * cos_theta_t) / \
                     (ior_to * cos_theta_i + ior_from * cos_theta_t)

        return ((r_perpendicular ** 2) + (r_parallel ** 2)) / 2.0



_THIRD_AXE = { \
    'xy': 'z',
    'yx': 'z',
    'xz': 'y',
    'zx': 'y',
    'yz': 'x',
    'zy': 'x'}


class OrthonormalBasis():
    """Represents orthonormal basis of a 3D Vector Space with given axis versors
       with respect to natural basis."""

    x_axis = None
    y_axis = None
    z_axis = None

    def __init__(self, x_axis, y_axis, z_axis):
        """Creates orthonormal basis with given three versors.

           Caller is expected to assure that given versors are normalised and
           mutually orthogonal."""
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis

    def transform(self, vec):
        """ Transforms components of a given vector in natural basis to this
            basis."""
        return  self.x_axis * vec[0] + self.y_axis * vec[1] + self.z_axis * vec[2]

    @staticmethod
    def from_two(axes, first, second):
        """Uses two given vectors (they must be normalised) to construct
           orthonormal basis, setting respective axes according to axes
           parameter."""
        assert len(axes) == 2 and axes[0] != axes[1]

        third = first.cross(second).normalised()
        second = third.cross(first)

        kwargs = {}

        kwargs[axes[0] + '_axis'] = first
        kwargs[axes[1] + '_axis'] = second
        kwargs[_THIRD_AXE[axes] + '_axis'] = third

        return OrthonormalBasis(**kwargs)

    @staticmethod
    def from_z_axis(z_axis):
        """Creates orthonormal basis with given z axis (must be normalised) and
           arbitrary x- and y-axes."""
        x_axis = Vec3.versor(0)
        if abs(z_axis.dot(x_axis)) > 0.99:
            x_axis = Vec3.versor(1)
        x_axis = x_axis.cross(z_axis).normalised()
        y_axis = z_axis.cross(x_axis).normalised()
        return OrthonormalBasis(x_axis, y_axis, z_axis)



def sample_cone(direction, angle, u_pos, v_pos):
    """Gets a random direction from a cone specified by its direction axis and
       spread angle (with u, v params for uniform strided sampling)."""
    if angle < 0.00000001:
        return direction

    angle = angle * (1.0 - (2.0 * math.acos(u_pos) / math.pi))
    radius = math.sin(angle)
    z_scale = math.cos(angle)
    random_angle = v_pos * 2.0 * math.pi
    basis = OrthonormalBasis.from_z_axis(direction)
    raw_v = Vec3(math.cos(random_angle) * radius, \
                 math.sin(random_angle) * radius, \
                 z_scale)
    return basis.transform(raw_v).normalised()

def sample_hemisphere(basis, u_pos, v_pos):
    """Gets a random direction from a hemisphere defined by positive z-axis of
       given orthonormal basis (with u, v params for uniform strided sampling).
       """
    random_angle = 2.0 * math.pi * u_pos
    radius_sqr = v_pos
    radius = math.sqrt(radius_sqr)
    raw_v = Vec3(math.cos(random_angle) * radius, \
                 math.sin(random_angle) * radius, \
                 math.sqrt(1.0 - radius_sqr))
    return basis.transform(raw_v).normalised()
