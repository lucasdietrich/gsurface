from surface_guided_sim.model import Surface

from mayavi import mlab

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np


def mayavi_plot_surface(mesh: np.ndarray, trajectory: np.ndarray = None):
    mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    # mlab.mesh(*mesh, opacity=0.8, color=(0.6, 0.6, 0.6))  # , color=(0.1, 0.1, 0.6)
    # colormap=cool / warm / binary / gray
    mlab.mesh(*mesh, opacity=1.0, colormap='binary')  # , color=(0.1, 0.1, 0.6)
    mlab.mesh(*mesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')

    mlab.orientation_axes()

    if trajectory is not None:
        mlab.plot3d(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0), tube_radius=0.01)


def matplotlib_plot_surface(mesh: np.ndarray, trajectory: np.ndarray = None) -> Axes3D:
    fig = plt.figure(figsize=(6, 6))

    ax: Axes3D = fig.add_subplot(111, projection='3d')

    ul = np.max(mesh)
    ll = np.min(mesh)

    ax.set_xlim3d(ll, ul)
    ax.set_ylim3d(ll, ul)
    ax.set_zlim3d(ll, ul)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Plot the surface

    # color map : https://matplotlib.org/tutorials/colors/colormaps.html
    # ax.plot_wireframe()
    ax.plot_surface(*mesh, rstride=1, cstride=1, edgecolor=(0.3, 0.3, 0.3, 0.3), color=(0.9, 0.9, 0.9, 0.1), alpha=0.3, antialiased=True)

    if trajectory is not None:
        ax.plot3D(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0))
        ax.scatter3D(*trajectory[0, :], s=10, color=(0, 0, 1, 1))
        ax.scatter3D(*trajectory[-1, :], s=10, color=(1, 0, 0, 1))

    return ax
