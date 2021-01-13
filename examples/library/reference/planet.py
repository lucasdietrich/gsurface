from gsurface import Plan, NewtonGravity, SurfaceGuidedMassSystem, Tyi, build_s0, ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, matplotlib_plot_solutions

import numpy as np

# simulate a planet rotating around a fixed massive system

universe_def = Plan(c=1.0).setlims(u_ul=2.5, v_ul=2)
universe = universe_def.build_surface(*universe_def.mesh(50, 50))

model = SurfaceGuidedMassSystem(
    surface=universe_def,
    s0=build_s0(u0=1.0, dv0=0.5, du0=1.0),
    m=1.0,
    forces=[
        NewtonGravity(m=1.0, M=100.0, G=1.0, clip=np.zeros((3,))),
        # DistanceGravity(m=1.0, M=100.0, G=1.0, clip=np.array([1.0, 0.0, 0.0])),  # 2 mass objects
        # ViscousFriction(0.1)  # friction
    ]
)

time = np.linspace(0, 20, 3000)

data = model.solve(time)

solutions = model.solutions(data, time)

matplotlib_plot_solutions(time, data, solutions)
mayavi_plot_surfaces([
    SurfacePlot(universe, trajectory=solutions[Tyi])
])