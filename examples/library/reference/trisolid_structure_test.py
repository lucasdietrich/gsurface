import numpy as np

from gsurface import Tyi
from gsurface.advanced.structure import SurfaceGuidedStructureSystem, TriangleStructure
from gsurface.forces import ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab
from gsurface.surface import Plan

surface = Plan(0.0, 0.0, 1.0)
mesh = surface.build_surface(*surface.mesh(50, 50))

structure = TriangleStructure(totalMass=4.0, stiffness=1000.0, mu=10.0, l0=0.5)

structure[1, 2].l0 = 0.8
structure.nodes[0].mass = 100.0

model = SurfaceGuidedStructureSystem(surface, structure, [
    ViscousFriction(1.0)
])

time = np.linspace(0, 2, 1000)

states = model.solve(time)

solutions = list(model.solutions(states, time))

mayavi_plot_surfaces([
    SurfacePlot(mesh, showSurface=(i == 0), trajectory=solutions[i][Tyi][::5]) for i in range(model.degree)
])
mlab.view(0, 0, 5.0, np.zeros((3,)))
