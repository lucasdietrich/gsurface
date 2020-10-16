# two models of sphere of different size with one mass on each, force between this two masses

import time as timelib

import numpy as np
from ode import solver

from gsurface.forces import Gravity, ViscousFriction
from gsurface.indexes import Tyi
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.plotter.mayavi import mlab, mayavi_plot_surfaces, SurfacePlot
from gsurface.surface import Sphere, Tore

# object 1
sphere = Sphere(1.0)
mesh_sphere = sphere.build_surface(*sphere.mesh(50, 50))

# object 2
tore = Tore(r=0.5, R=1.0).translate(np.array([3.0, 0.0, 0.0]))
mesh_tore = tore.build_surface(*tore.mesh(50, 50))

# setup simulation for tore
tore_sim = SurfaceGuidedMassSystem(
    surface=tore,
    s0=build_s0(du0=10.0),
    m=1.0,
    forces=[
        Gravity(1.0, np.array([0.0, 0.0, -9.0])),
        ViscousFriction(0.5)
    ]
)

# setup simulation for sphere
sphere_sim = SurfaceGuidedMassSystem(
    surface=sphere,
    s0=build_s0(u0=1.5, du0=10.0, v0=1.5),
    m=1.0,
    forces=[
        Gravity(1.0, np.array([0.0, 0.0, +9.0])),
        ViscousFriction(0.5)
    ]
)

if __name__ == "__main__":
    print(tore_sim)
    print(sphere_sim)

    time = np.linspace(0.0, 10.0, 1000)

    # concept:

    # joint_sim = SpringInteraction(sphere_sim, tore_sim).export_simulation()

    # # equivalent definition to

    # joint_sim = SurfaceGuidedInteractedMassSystems([
    #   sphere_sim,
    #   tore_sim,
    #   other_sim,
    # ], [
    #   SpringInteraction(sphere_sim, tore_sim),
    #   SpringInteraction(tore_sum, other_sim),
    # ])

    # data = joint_sim.solve(time, solver=solver.rk4)
    # solutions = joint_sim.solutions(data, time)

    t1 = timelib.time()
    tore_data = tore_sim.solve(time, solver=solver.rk4)
    tore_solutions = tore_sim.solutions(tore_data, time)

    sphere_data = sphere_sim.solve(time, solver=solver.rk4)
    sphere_solutions = sphere_sim.solutions(sphere_data, time)
    t2 = timelib.time()

    print(t2 - t1)

    # plot
    mayavi_plot_surfaces([
        SurfacePlot(mesh_sphere, trajectory=sphere_solutions[Tyi]),
        SurfacePlot(mesh_tore, trajectory=tore_solutions[Tyi])
    ])
    mlab.show()

