from surface_guided_sim.model import Surface

from mayavi import mlab

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np


def mayavi_plot_surface(mesh: np.ndarray):
    mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    mlab.mesh(*mesh, opacity=0.8, color=(0.6, 0.6, 0.6))  # , color=(0.1, 0.1, 0.6)
    mlab.mesh(*mesh, opacity=0.3, color=(0, 0, 0), representation='wireframe')

    mlab.orientation_axes()


def matplotlib_plot_surface(mesh: np.ndarray) -> Axes3D:
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection='3d')

    ul = np.max(mesh)
    ll = np.min(mesh)

    ax.set_xlim3d(ll, ul)
    ax.set_ylim3d(ll, ul)
    ax.set_zlim3d(ll, ul)

    # Plot the surface
    ax.plot_surface(*mesh, color=(0.6, 0.6, 0.6, 0.8), rstride=1, cstride=1)

    return ax
