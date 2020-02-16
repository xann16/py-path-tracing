"""Executable script for path tracing renderer module."""

from .oop.vector import Vec3
from .oop.utils import load_params
from .oop.scene_settings import MaterialData
from .oop.oop_renderer import Renderer, DEFAULT_RENDERER_PARAMS
from .oop.camera import Camera
from .oop.oop_scene import SceneBuilder


def create_sphere_scene(params):
    """Creates renderer for a scene with single sphere."""

    if params is None:
        params = DEFAULT_RENDERER_PARAMS

    cam_pos = Vec3(0, 0, -3.2)
    cam_look_at = Vec3(0, 0, 0)
    cam_up = Vec3(0, 1, 0)
    vertical_fov = 40
    cam = Camera(cam_pos, cam_look_at, cam_up,
                 params['width'], params['height'],
                 vertical_fov)

    scb = SceneBuilder(Vec3())

    light_radius = 3
    light_offset = Vec3(6, 6, 0)
    light_mat = MaterialData.make_light(Vec3(8, 8, 8))
    scb.add_sphere(cam_pos + light_offset - Vec3(0, 0, light_radius), light_radius, light_mat)

    sph_mat = MaterialData.make_diffuse(Vec3(0.2, 0.2, 0.2))
    sph_mat.refraction_index = 1.3
    sph_mat.reflection_cone_angle = 0.05
    scb.add_sphere(Vec3(), 1, sph_mat)

    sky_mat = MaterialData.make_diffuse(Vec3(0.2, 0.2, 0.5))
    scb.add_sphere(Vec3(), 10, sky_mat)

    return Renderer(scb.scene, cam, params)

def create_spheres_scene(params):
    """Creates renderer for a scene with two spheres."""

    if params is None:
        params = DEFAULT_RENDERER_PARAMS

    cam_pos = Vec3(0, 0, -3.2)
    cam_look_at = Vec3(0, 0, 0)
    cam_up = Vec3(0, 1, 0)
    vertical_fov = 40
    cam = Camera(cam_pos, cam_look_at, cam_up,
                 params['width'], params['height'],
                 vertical_fov)

    scb = SceneBuilder(Vec3())

    light_radius = 3
    light_offset = Vec3(6, 6, 0)
    light_mat = MaterialData.make_light(Vec3(8, 8, 8))
    scb.add_sphere(cam_pos + light_offset - Vec3(0, 0, light_radius), light_radius, light_mat)

    sph_mat = MaterialData.make_diffuse(Vec3(0.2, 0.2, 0.2))
    sph_mat.refraction_index = 1.3
    sph_mat.reflection_cone_angle = 0.05
    scb.add_sphere(Vec3(0.5, 0, 0), 0.4, sph_mat)

    sph2_mat = MaterialData.make_diffuse(Vec3(0.4, 0.4, 0.4))
    sph2_mat.refraction_index = 1.5
    sph2_mat.reflection_cone_angle = 0.1
    scb.add_sphere(Vec3(-0.5, 0, 0), 0.4, sph2_mat)

    sky_mat = MaterialData.make_diffuse(Vec3(0.2, 0.2, 0.5))
    scb.add_sphere(Vec3(), 10, sky_mat)

    return Renderer(scb.scene, cam, params)


SCENES = { \
    'sphere' : create_sphere_scene,
    'spheres' : create_spheres_scene}


def create_renderer(scene_name, params_path=None):
    """Creates renderer from given scene_name and optional path to parameters
       json file."""
    assert scene_name in SCENES, "Unknown scene name"
    params = load_params(params_path) if params_path else None
    return SCENES[scene_name](params)

def render_to_png(renderer, output_path, verbose):
    """Uses given renderer to render its scene and save it to given destination
       path as png file."""
    output = renderer.render(verbose)
    output.save_as_png(output_path)
    if verbose:
        print("Renderes image saved as '{}'.".format(output_path))
