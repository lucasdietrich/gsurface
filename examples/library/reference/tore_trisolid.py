from gsurface.advanced.structure import SurfaceGuidedStructureSystem, TriangleStructure
from gsurface.surface import Tore
from gsurface.forces import Gravity, ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab

from gsurface import Tyi

import numpy as np

surface = Tore()
mesh = surface.build_surface(*surface.mesh(50, 50))

structure = TriangleStructure(totalMass=4.0, stiffness=1000.0, mu=10.0, l0=0.5)

model = SurfaceGuidedStructureSystem(surface, structure, [
    Gravity(1.0, np.array([0.0, 0.0, -9.81])),
    ViscousFriction(1.0)
])

model.s0[1] = 5.0
model.s0[3] = 25.0

time = np.linspace(0, 10, 1000)

states = model.solve(time)

solutions = list(model.solutions(states, time))

mayavi_plot_surfaces([
    SurfacePlot(mesh, showSurface=(i == 0), trajectory=solutions[i][Tyi]) for i in range(model.degree)
])
mlab.view(45, 45, 10.0, np.zeros((3,)))