from typing import Tuple, Callable

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(0, 2 * np.pi, 100)
r = np.linspace(0, 1, 100)

rmesh, tmesh = np.meshgrid(r, theta)

z = rmesh**2
x = rmesh * np.sin(tmesh)
y = rmesh * np.cos(tmesh)

ax.plot_wireframe(x, y, z, rstride=10, cstride=10)

plt.show()
