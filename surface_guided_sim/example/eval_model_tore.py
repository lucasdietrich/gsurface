from surface_guided_sim.model import *
from surface_guided_sim.surface import SurfaceTore

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np

tore = SurfaceTore(0.5, 1.0)

fig = plt.figure()
ax: Axes3D = fig.add_subplot(111, projection='3d')

angle = np.linspace(0, 2*np.pi, 50)

# u, v = np.meshgrid(angle, angle)

M = np.zeros((3, 50, 50))

for i, u in enumerate(angle):
    for j, v in enumerate(angle):
        M[:, i, j] = tore.eval(u, v)

# https://stackoverflow.com/questions/31768031/plotting-points-on-the-surface-of-a-sphere-in-pythons-matplotlib
ax.scatter(*tore.eval(0, 0), c="red", s=30, zorder=10)

ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-2, 2)

# Plot the surface
ax.plot_surface(*M, color=(0.8, 0.8, 0.8, 0.7), rstride = 2, cstride = 1)

plt.show()



sim = SurfaceGuidedFallSystem(tore)

print(sim._derivs(sim.s0, 0))