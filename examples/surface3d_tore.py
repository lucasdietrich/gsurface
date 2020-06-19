from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# tore : https://fr.wikipedia.org/wiki/Tore

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

r = 0.25
R = 0.5

# Make data
angle = np.linspace(0, 2*np.pi, 50)

u, v = np.meshgrid(angle, angle)

x = (R + r*np.cos(v)) * np.cos(u)
y = (R + r*np.cos(v)) * np.sin(u)
z = r * np.sin(v)

ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)

# Plot the surface
ax.plot_surface(x, y, z, color=(0.8, 0.8, 0.8, 1), rstride = 2, cstride = 1)

plt.show()
