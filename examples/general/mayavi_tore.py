from mayavi import mlab
import numpy as np

r = 0.5
R = 1.0

u, v = np.mgrid[0:2*np.pi:25j, 0:2*np.pi:50j]

x = (R + r*np.cos(v)) * np.cos(u)
y = (R + r*np.cos(v)) * np.sin(u)
z = r * np.sin(v)

mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
mlab.clf()

# https://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html#mesh
mlab.buildsurface(x, y, z, opacity=0.8) # , color=(0.1, 0.1, 0.6)
mlab.buildsurface(x, y, z, opacity=0.8, color=(0, 0, 0), representation='wireframe')
mlab.points3d(1.5, 0, 0, color=(1.0, 0.0, 0.0), scale_factor=0.1)

mlab.orientation_axes()

mlab.show()