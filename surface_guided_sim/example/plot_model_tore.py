from surface_guided_sim.model import *
from surface_guided_sim.surface import Tore

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mayavi import mlab

from surface_guided_sim.plotter import matplotlib_plot_surface, mayavi_plot_surface

import numpy as np

tore = Tore(0.5, 1.0)

######################################
# Simulation
######################################
sim = SurfaceGuidedFallSystem(tore)

# check this
sim.s0 = np.array([
    1.0, 1.0,
    np.pi/2 - 1.0, 0.0
])

sim.s0 = np.array([
    1.0, 0.2,
    0.0, 2.0
])

time = np.linspace(0, 8, 1000)

data = sim.solve(time)

# rebuild all evals
evals = sim.surface.trajectory(data[:, 0::2])

######################################
# Plot
######################################
U, V = np.linspace(0, 2*np.pi, 80), np.linspace(0, 2*np.pi, 20)
mesh = tore.buildsurface(U, V)


if 1:
    mayavi_plot_surface(mesh)
    mlab.plot3d(evals[:, 0], evals[:, 1], evals[:, 2], color=(1, 0, 0), tube_radius=0.01)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("position")
    plt.xlabel("time (sec)")
    plt.ylabel("parameters")
    plt.plot(time, data[:, 0::2])
    plt.legend(["u", "v"])
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.title("speed")
    plt.xlabel("time (sec)")
    plt.ylabel("dt parameters")
    plt.plot(time, data[:, 1::2])
    plt.legend(["du", "dv"])
    plt.grid(True)

    plt.show()  # work for matplotlib & mlab

