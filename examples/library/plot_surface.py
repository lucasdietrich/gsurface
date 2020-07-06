from surface_guided_sim.surface import Sphere, Plan, Tore, Catenoid, EggBox, ConicalCorner

from surface_guided_sim.plotter import mayavi_plot_surface, mlab

surface = Catenoid(1.0)

mesh = surface.mesh(50, 50)
mesh_surface = surface.buildsurface(*mesh)

mayavi_plot_surface(mesh_surface, plot_style=0)

mlab.show()
