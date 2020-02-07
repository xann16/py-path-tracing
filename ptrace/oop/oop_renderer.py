"""Encapsulates monte carlo path tracing rendering engine."""

import random

from .vector import Vec3
from.image_output import AccumulableImage

## Hardcoded renderer parameters:
DEFAULT_RENDERER_PARAMS = { \
    'width': 1920,
    'height': 1080,
    'preview': False,
    'samples_per_pixel': 40,
    'max_cpus': 1,
    'max_depth': 5,
    'first_bounce_u_samples': 4,
    'first_bounce_v_samples': 4}


#pylint: disable=too-few-public-methods

class RadianceSampler():
    """Encapsulates iterative sampling of consecutive light ray hits."""

    renderer = None
    depth = 0

    def __init__(self, renderer, depth=0):
        """Initializes sampler for given renderer at given depth."""
        self.renderer = renderer
        self.depth = depth

    def __call__(self, ray):
        """Performs sampling using current renderer and depth setting."""
        return self.renderer.radiance(ray, self.depth)

#pylint: enable=too-few-public-methods



class Renderer():
    """Rendering engine for monte carlo path tracing method."""

    scene = None
    camera = None
    params = None

    def __init__(self, scene, camera, params=None):
        """Initializes renderer with given scene, camera, and parameters."""
        self.scene = scene
        self.camera = camera
        self.params = params if params is not None else DEFAULT_RENDERER_PARAMS

    def render(self, verbose=False):
        """Renders scene returns accumulable image."""

        height = self.params['height']
        width = self.params['width']
        samples = self.params['samples_per_pixel']

        if verbose:
            print("Rendering... Sampling passes done:  0/{:2}".format(samples), end='')

        output = AccumulableImage(width, height)
        for sample in range(1, samples + 1):
            for x_pos, y_pos in zip(range(0, width), range(0, height)):
                ray = self.camera.get_ray(x_pos, y_pos)
                output.add_samples(x_pos, y_pos, self.radiance(ray, 0), 1)
            if verbose:
                print("\rRendering... Sampling passes done: {:2}/{:2}".format(sample, samples),
                      end='')
        if verbose:
            print("\rRendering done.")

        return output

    #pylint: disable=no-self-use

    def render_tiled(self):
        """Renders scene in a tiled mode using given update function and returns
           accumulable image."""
        assert False, "Not yet implemented!"

    #pylint: enable=no-self-use

    def radiance(self, ray, depth):
        """Probes light for given ray and given maximal depth."""

        if depth >= self.params['max_depth']:
            return Vec3()

        u_samples = self.params['first_bounce_u_samples'] if depth == 0 else 1
        v_samples = self.params['first_bounce_v_samples'] if depth == 0 else 1

        hit = self.scene.intersect_ex(ray)
        if hit is None:
            return self.scene.environment_colour

        material = hit['material']
        if self.params['preview']:
            return material.preview_colour()
        hit = hit['hit_record']

        result = Vec3()
        sampler = RadianceSampler(self, depth + 1)

        # even sampling with random offset
        for u_ix, v_ix in zip(range(0, u_samples), range(0, v_samples)):
            u_pos = (u_ix + random.random()) / u_samples
            v_pos = (v_ix + random.random()) / v_samples
            prob = random.random()

            result += material.sample(hit, ray, sampler, u_pos, v_pos, prob)

        return material.totalEmission(result / (u_samples * v_samples))

    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals

    def generate_tiles(self, x_size, y_size, sample_count, samples_per_tile, width=-1, height=-1):
        """Generates tiles for tiled rendering."""
        if width < 0:
            width = self.params.width
        if height < 0:
            height = self.params.height

        x_centre = width / 2
        y_centre = height / 2

        tiles = []
        for y_pos in range(0, height, y_size):
            y_beg = y_pos
            y_end = min(y_pos + y_size, height)
            for x_pos in range(0, width, x_size):
                x_beg = x_pos
                x_end = min(x_pos + x_size, width)
                x_mid = int(x_beg + x_end / 2)
                y_mid = int(y_beg + y_end / 2)
                dist_sqr = int(((x_mid - x_centre) ** 2) + ((y_mid - y_centre) ** 2))
                for samples in range(0, sample_count, samples_per_tile):
                    n_sampl = min(samples + samples_per_tile, sample_count) - samples
                    tiles.append({ \
                        'x_range': (x_beg, x_end),
                        'y_range': (y_beg, y_end),
                        'samples': n_sampl,
                        'sample_ix': samples,
                        'dist_prio': dist_sqr,
                        'rand_prio': random.random()})
        return sorted(tiles, key=lambda x: (x['sample_ix'], x['dist_prio'], x['rand_prio']))

    #pylint: enable=too-many-locals
    #pylint: enable=too-many-arguments
