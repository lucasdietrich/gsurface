"""

This example show how to create a surface and plot it

"""

from gsurface.plotter import mayavi_plot_surface
from gsurface.surface import Catenoid

surface = Catenoid(1.0)

# create u, v mesh
mesh = surface.mesh(50, 50)

# create surface mesh
mesh_surface = surface.build_surface(*mesh)

# plot
mayavi_plot_surface(mesh_surface, surface_plot_style=0)
