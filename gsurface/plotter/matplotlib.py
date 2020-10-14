from ..indexes import *

from typing import Tuple, Iterable

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np


def _matplotlib_subplot_curves(
        time: np.ndarray,
        tvector: np.ndarray,
        subplot: Tuple,
        title: str,
        ylabel: str,
        legends: Iterable[str]
):
    plt.subplot(*subplot)
    plt.plot(time, tvector)
    plt.title(title)
    plt.xlabel("time (sec)")
    plt.ylabel(ylabel)
    plt.legend(legends)
    plt.grid(True)


def matplotlib_plot_solutions(time: np.ndarray, states: np.ndarray, physics: np.ndarray):
    assert time.shape[0] == physics.shape[0]

    plt.figure(figsize=(18, 9))

    plt.subplots_adjust(left=0.08, bottom=0.08, right=1 - 0.04, top=1 - 0.04, wspace=0.1, hspace=0.2)

    _matplotlib_subplot_curves(time, physics[:, Si], (2, 3, 1), "Trajectory", "position (m)", ["X", "Y", "Z"])
    _matplotlib_subplot_curves(time, physics[:, Vi], (2, 3, 2), "Speed", "speed (m/s)", ["Vx", "Vy", "Vz"])
    _matplotlib_subplot_curves(time, physics[:, Eki: Emi + 1], (2, 3, 3), "Energies", "Energy (J)", ["Ek", "Ep", "Em"])
    _matplotlib_subplot_curves(time, physics[:, Fi], (2, 3, 4), "SumForce", "force (N)", ["Fx", "Fy", "Fz"])
    _matplotlib_subplot_curves(time, physics[:, nVi], (2, 3, 5), "Absolute speed", "speed (m/s)", ["V"])
    _matplotlib_subplot_curves(time, states[:, 1::2], (2, 3, 6), "Parametric speed", "(1/s)", ["du", "dv", "norm w"])

    plt.show()


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
