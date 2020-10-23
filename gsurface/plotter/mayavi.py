from mayavi import mlab

import numpy as np

from ..indexes import *

from typing import Iterable, List, Tuple, Union

from dataclasses import dataclass

# try color : (0.1, 0.1, 0.6)
# colormap=cool / warm / binary / gray

mayavi_plot_surface_styles = [
    # style 0
    [
        # two layers (surface + mesh)
        {
            "opacity": 0.3,
            "colormap": 'cool',
        },
        {
            "opacity": 0.1,
            "color": (0, 0, 0),
            "representation": 'wireframe',
        }
    ],
    # style 1
    [
        # two layers (surface + mesh)
        {
            "opacity": 1.0,
            "colormap": 'binary',
        },
        {
            "opacity": 0.1,
            "color": (0, 0, 0),
            "representation": 'wireframe',
        }
    ],
    # style 2 : don't show
    [

    ]
]

ColorType = Tuple[float, float, float]


@dataclass
class SurfacePlot:

    # surface plot
    smesh: np.ndarray = None
    showSurface: bool = True

    surfaceStyle: int = 0

    # trajectory plot
    trajectory: np.ndarray = None
    trajectoryColor: ColorType = (1, 0, 0)
    showTrajectory: bool = True

    # solid for animation
    solidColor: ColorType = (0, 0, 1)
    showSolid: bool = True
    animate: bool = True

    # todo physic post computed solutions and chart display
    physics: np.ndarray = None
    display_physics: bool = False


def mayavi_plot_surfaces(surface_plots: List[SurfacePlot], animationDelay: int = 10, show=True):
    """
    Plot a set of surfaces (surface with style, trajectory, animation)
    :param animationDelay:
    :param show:
    :param surface_plots:
    :return:
    """
    mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    # list of animated points with trajectory
    animated_solids = []

    time_iterations = None

    for splot in surface_plots:
        # if surface is
        if splot.smesh is not None and splot.showSurface:
            # load style
            try:
                style_set = mayavi_plot_surface_styles[splot.surfaceStyle]
            except IndexError:
                raise Exception("plot_style undefined")

            # plot surface with styles
            for style in style_set:
                mlab.mesh(*splot.smesh, **style)

        # add trajectory
        if splot.trajectory is not None:
            # todo fix error when animation does not work when showTrajectory is False
            if splot.showTrajectory:
                mlab.plot3d(splot.trajectory[:, 0], splot.trajectory[:, 1], splot.trajectory[:, 2],
                            color=splot.trajectoryColor, tube_radius=0.01)

            if splot.showSolid:
                solid = mlab.points3d(*splot.trajectory[0], color=splot.solidColor, scale_factor=0.1)

                if splot.animate:
                    # get time iterations
                    time_iterations = splot.trajectory.shape[0]

                    # animate trajectory
                    animated_solids.append((solid, splot.trajectory))

    mlab.orientation_axes()

    # add animation
    if animated_solids:
        @mlab.animate(delay=animationDelay)
        def anim():
            while True:
                for i in range(time_iterations):
                    for solid, traj in animated_solids:
                        x, y, z = traj[i]
                        solid.mlab_source.set(x=x, y=y, z=z)
                    yield

        if show:
            anim()
    elif show:
        mlab.show()


# retrocompatibility
def mayavi_plot_surface(smesh: np.ndarray, trajectory: np.ndarray = None, surface_plot_style=0):
    sp = SurfacePlot(smesh=smesh, trajectory=trajectory, surfaceStyle=surface_plot_style, animate=False)
    return mayavi_plot_surfaces([sp])


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
