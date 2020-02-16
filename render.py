"""Executable script for path tracing renderer module."""

import sys
import time

from ptrace.core import create_renderer, render_to_png


if __name__ == '__main__':
    scene_name = 'sphere'
    params = None
    verbose = False
    output_path = None

    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
        for arg in sys.argv[2:]:
            if arg.startswith('-p'):
                params = arg.strip().split('=', 1)[1]
            elif arg.startswith('-v'):
                verbose = True
            elif arg.startswith('-o'):
                output_path = arg.strip().split('=', 1)[1]
            else:
                assert False, 'Unknown command line argument.'
    if not output_path:
        output_path = './' + scene_name + '.png'

    renderer = create_renderer(scene_name, params)

    if verbose:
        print("Rendering scene '{}' ({}x{}) to: {}".format(scene_name,
                                                           renderer.params['width'],
                                                           renderer.params['height'],
                                                           output_path))
        start_time = time.time()

    render_to_png(renderer, output_path, verbose)

    if verbose:
        print("Time elapsed: {} s.".format(time.time() - start_time))
