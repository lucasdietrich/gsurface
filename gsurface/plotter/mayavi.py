from mayavi import mlab

import numpy as np

from ..indexes import *


def mayavi_plot_surface(smesh: np.ndarray, trajectory: np.ndarray = None, surface_plot_style=0):
    mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    # colormap=cool / warm / binary / gray
    if surface_plot_style == 0:
        mlab.mesh(*smesh, opacity=0.3, colormap='cool')  # , color=(0.1, 0.1, 0.6)
        mlab.mesh(*smesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')
    elif surface_plot_style == 1:
        mlab.mesh(*smesh, opacity=1.0, colormap='binary')  # , color=(0.1, 0.1, 0.6)
        mlab.mesh(*smesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')
    else:
        raise Exception("plot_style undefined")

    if trajectory is not None:
        mlab.plot3d(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0), tube_radius=0.01)
        mlab.points3d(*trajectory[0], color=(0, 0, 1), scale_factor=0.05)

    mlab.orientation_axes()


def mayavi_animate_surface_trajectory(smesh: np.ndarray, trajectory: np.ndarray = None, abs_speed: np.ndarray = None):
    mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    mlab.mesh(*smesh, opacity=0.3, colormap='cool')  # , color=(0.1, 0.1, 0.6)
    mlab.mesh(*smesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')

    solid_point = mlab.points3d(*trajectory[0], color=(1, 0, 0), scale_factor=0.05)
    mlab.plot3d(trajectory[:, xi], trajectory[:, yi], trajectory[:, zi], abs_speed, tube_radius=0.01)

    mlab.orientation_axes()

    @mlab.animate(delay=10)
    def anim():
        while True:
            for i, (x, y, z) in enumerate(trajectory):
                solid_point.mlab_source.set(x=x, y=y, z=z)
                # mlab.savefig("./temp/f{0}.png".format(i))
                yield

    return anim
