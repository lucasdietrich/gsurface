from time import time

import numpy as np

from gsurface.plotter.mayavi import SurfacePlot, mayavi_plot_surfaces
from gsurface.surface import Cylinder, Sphere

cyl = Cylinder(R=1.0).translate(np.array([0.0, 0.0, 1.0]))

half_sph = Sphere(R=1.0).setlims(u_ul=np.pi)

cyl_surf = cyl.build_surface(*cyl.mesh(50, 50))
half_sph_surf = half_sph.build_surface(*half_sph.mesh(50, 50))

a = time()
area = cyl.area()
b = time()

print(cyl, cyl.area(), f"theorical surface = 2*pi {b - a:.3f}ms")
print(half_sph, half_sph.area(), "theorical surface = 4*pi/2 = 2*pi (half sphere)")

mayavi_plot_surfaces([
    SurfacePlot(cyl_surf),
    SurfacePlot(half_sph_surf)
])