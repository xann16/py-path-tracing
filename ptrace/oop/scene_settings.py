"""Classes for lading and storage of scene setting and objects."""

from .utils import deg2rad
from .vector import Vec3


class MaterialData():
    """Describes properties of a material attributed to scene geometry."""

    emission = None
    diffuse = None
    refraction_index = 1.0
    reflectivity = -1.0
    reflection_cone_angle = 0.0

    #pylint: disable=too-many-arguments

    def __init__(self, emission=None, diffuse=None,
                 refraction_index=1.0,
                 reflectivity=-1.0,
                 reflection_cone_angle=0.0):
        """Creates material with default or given settings."""
        self.emission = emission if emission is not None else Vec3()
        self.diffuse = diffuse if diffuse is not None else Vec3()
        self.refraction_index = refraction_index
        self.reflectivity = reflectivity
        self.reflection_cone_angle = reflection_cone_angle

    #pylint: enable=too-many-arguments

    @staticmethod
    def make_diffuse(colour):
        """Creates basic diffuse material with given colour."""
        return MaterialData(diffuse=colour)

    @staticmethod
    def make_specular(colour, intensity):
        """Creates basic specular material with given colour and specular
           highlight intensity."""
        return MaterialData(diffuse=colour, refraction_index=intensity)

    @staticmethod
    def make_light(colour):
        """Creates basic material for light source of given colour."""
        return MaterialData(emission=colour)

    @staticmethod
    def make_glossy(colour, intensity, cone_angle_deg):
        """Creates glossy material with given colour, intensity, and angle of
           specular reflection in degrees."""
        return MaterialData(diffuse=colour, refraction_index=intensity,
                            reflection_cone_angle=deg2rad(cone_angle_deg))

    @staticmethod
    def make_reflective(colour, reflectivity, cone_angle_deg):
        """Creates reflective material with given colour, reflectivity, and
           angle of reflection in degrees."""
        return MaterialData(diffuse=colour, reflectivity=reflectivity,
                            reflection_cone_angle=deg2rad(cone_angle_deg))

    def __eq__(self, other):
        """Checks whether two material are equal."""
        return self.emission == other.emission and \
               self.diffuse == other.diffuse and \
               self.refraction_index == other.refraction_index and \
               self.reflectivity == other.reflectivity and \
               self.reflection_cone_angle == other.reflection_cone_angle

    def __ne__(self, other):
        """Checks whether two material are not equal."""
        return not self == other


# HARDCODED MATERIALS FOR TEST SCENES:

MATERIAL_DATA = { \
    'suzanne': { \
        'suzanne' : MaterialData.make_specular(Vec3(0.247, 0.788, 0.298), 1.3)}}
