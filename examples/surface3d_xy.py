from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data
u = np.linspace(-1, 1, 100)
v = np.linspace(-1, 1, 100)

x, y = np.meshgrid(u, v)

z = x*y

# Plot the surface
ax.plot_surface(x, y, z, color=(0.2, 0, 0.5, 0.5))

plt.show()
