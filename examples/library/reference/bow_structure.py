import numpy as np

from gsurface import Tyi
from gsurface.advanced.structure import BowStructure, SurfaceGuidedStructureSystem
from gsurface.forces import ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot
from gsurface.plotter.colors import rgb
from gsurface.surface import Tore

SIZE = 5

surface = Tore(0.5, 1.0)
mesh = surface.build_surface(*surface.mesh(50, 50))

snake = BowStructure(SIZE, 1.0, stiffness=1000.0, mu=10.0, l0=1.0)

snake.interactions[(0, SIZE - 1)].stiffness = 100.0

sim = SurfaceGuidedStructureSystem(surface, snake, structureForces=[
    ViscousFriction(0.01)
])

sim.s0[1::4] = 1.0

time = np.linspace(0, 40, 1000)

data = sim.solve(time)

solutions = sim.solutions(data, time)

mayavi_plot_surfaces([
    SurfacePlot(
        smesh=mesh,
        showSurface= i == 0,
        trajectory=solution[Tyi],
        trajectoryColor=rgb[i % len(rgb)],
        showTrajectory=True
    ) for i, solution in enumerate(solutions)
])
