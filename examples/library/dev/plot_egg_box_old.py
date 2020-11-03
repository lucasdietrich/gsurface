from gsurface.model import *
from gsurface.surface import EggBox
from gsurface.forces import Gravity

import numpy as np

from gsurface.plotter import mayavi_plot_surface

import matplotlib.pyplot as plt

surface = EggBox(1).multlims(2.0)

######################################
# Simulation
######################################
s0 = np.array([
    0.0, 0.1,
    0.0, 0.2
])

g = np.array([
    0.0,
    0.0,
    -1.0
])

sim = SurfaceGuidedMassSystem(surface, s0, 1.0, [Gravity(m=1.0, g=g)])

time = np.linspace(0, 10, 20000)

states = sim.solve(time)

physics = sim.solutions(states, time)

trajectory = physics[:, Pi]
speed = physics[:, Vi]


######################################
# Plot
######################################
U, V = surface.mesh(200, 200)
surface_mesh = surface.build_surface(U, V)

# matplotlib_plot_surface(surface_mesh, trajectory)
mayavi_plot_surface(surface_mesh, trajectory)

plt.figure()
plt.subplot(1, 2, 1)
plt.title("position")
plt.xlabel("time (sec)")
plt.ylabel("parameters")
plt.plot(time, states[:, 0::2])
plt.legend(["u", "v"])
plt.grid(True)

plt.subplot(1, 2, 2)
plt.title("speed")
plt.xlabel("time (sec)")
plt.ylabel("dt parameters")
plt.plot(time, states[:, 1::2])
plt.legend(["du", "dv"])
plt.grid(True)

plt.show()  # work for matplotlib & mlab

