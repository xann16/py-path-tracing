"""Materials used to render scene geometry."""

from .raycast_base import Ray
from .vector import OrthonormalBasis, sample_cone, sample_hemisphere


class Material():
    """Base class for specific materials."""

    material_data = None

    def preview_colour(self):
        """Returns raw material diffuse colour."""
        return self.material_data.diffuse

    def total_emission(self, inbound):
        """Returns total amount light emitted, given inbound radiance."""
        return self.material_data.emission + inbound


#pylint: disable=too-many-arguments

class MatteMaterial(Material):
    """Represents data and functionality of a matte material (diffuse + basic
       specular) used to render scene geometry."""

    def __init__(self, material_data):
        """Creates instance of matte material."""
        self.material_data = material_data

    def sample(self, hit_record, incoming_ray, radiance_sampler, u_pos, v_pos, prob):
        """Samples material for emitted light given ray collision record,
           incoming ray, specific radiance sampling finction (Ray -> Vec3),
           as well as uniform u, v coordinates and preset sampling probability.
           """
        ior_from = 1.0
        ior_to = self.material_data.refraction_index
        if hit_record.is_inside:
            ior_from, ior_to = ior_to, ior_from

        reflectivity = hit_record.normal.reflectance(incoming_ray.direction, ior_from, ior_to)

        # specular reflection
        if prob < reflectivity:
            return radiance_sampler(Ray(hit_record.position, \
                    sample_cone(hit_record.normal.reflect(incoming_ray.direction), \
                                self.material_data.reflection_cone_angle, u_pos, v_pos)))

        # diffuse reflection
        basis = OrthonormalBasis.from_z_axis(hit_record.normal)
        return self.material_data.diffuse * \
                     radiance_sampler(Ray(hit_record.position, \
                                      sample_hemisphere(basis, u_pos, v_pos)))


class ShinyMaterial(Material):
    """Represents data and functionality of a shiny material (with reflections)
       used to render scene geometry."""

    def __init__(self, material_data):
        """Creates instance of matte material."""
        self.material_data = material_data

    def sample(self, hit_record, incoming_ray, radiance_sampler, u_pos, v_pos, prob):
        """Samples material for emitted light given ray collision record,
           incoming ray, specific radiance sampling finction (Ray -> Vec3),
           as well as uniform u, v coordinates and preset sampling probability.
           """

        # specular reflection
        if prob < self.material_data.reflectivity:
            return radiance_sampler(Ray(hit_record.position, \
                    sample_cone(hit_record.normal.reflect(incoming_ray.direction), \
                                self.material_data.reflection_cone_angle, u_pos, v_pos)))

        basis = OrthonormalBasis.from_z_axis(hit_record.normal)
        return self.material_data.diffuse * \
                radiance_sampler(Ray(hit_record.position, \
                                 sample_hemisphere(basis, u_pos, v_pos)))

#pylint: enable=too-many-arguments


def material_from_data(material_data):
    """Creates appropriate material based on given data."""
    if material_data.reflectivity >= 0.0:
        return ShinyMaterial(material_data)
    return MatteMaterial(material_data)
