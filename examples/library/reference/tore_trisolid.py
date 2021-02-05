# reference design for SurfaceGuidedStructureSystem

import numpy as np

from gsurface import Tyi
from gsurface.advanced.structure import SurfaceGuidedStructureSystem, TriangleStructure
from gsurface.forces import Gravity, ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab, rgb
from gsurface.surface import Tore

surface = Tore()
mesh = surface.build_surface(*surface.mesh(50, 50))

structure = TriangleStructure(totalMass=4.0, stiffness=1000.0, mu=10.0, l0=0.5)

structure[(0, 1)].l0 = 0.35

model = SurfaceGuidedStructureSystem(surface, structure, [
    Gravity(1.0, np.array([0.0, 0.0, -9.81])),
    ViscousFriction(1.0)
])

model.s0 = np.array([ 4.73114640e-01,  5.00000000e+00,  2.81624913e-02,  2.50000000e+01,
       -1.60399682e-02,  0.00000000e+00, -2.36683950e-01,  0.00000000e+00,
       -1.20742294e-01,  0.00000000e+00,  3.40214807e-01,  0.00000000e+00])

model.s0[1::4] = 2.0

time = np.linspace(0, 10, 1000)

states = model.solve(time)

solutions = model.solutions(states, time)

splot = [
    SurfacePlot(mesh, showSurface=(i == 0), solidColor=(1, 0.8, 0), trajectoryColor=rgb[i], trajectory=solution[Tyi]) for i, solution in enumerate(solutions)
]

mayavi_plot_surfaces(splot)
mlab.view(45, 45, 10.0, np.zeros((3,)))
