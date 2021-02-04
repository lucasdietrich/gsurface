from typing import Tuple, Callable

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


# function eval
p = np.linspace(0, 2, 100)

x = 1 - (p - 1)**2
z = 1 - (2*p - 1)**2

plt.figure()
plt.plot(x, z)
plt.show()

# surface eval

# theta = np.linspace(0, 2 * np.pi, 100)
#
# rmesh, tmesh = np.meshgrid(r, theta)
#
# z = rmesh**2
# x = rmesh * np.sin(tmesh)
# y = rmesh * np.cos(tmesh)
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
#
# ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
#
# plt.show()
