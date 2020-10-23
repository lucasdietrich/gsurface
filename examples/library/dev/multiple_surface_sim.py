# two models of sphere of different size with one mass on each, force between this two masses

import time as timelib

import numpy as np
from ode import solver

from gsurface.forces import Gravity, ViscousFriction, LengthedSpringForce, AirFriction
from gsurface.indexes import Tyi
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.plotter.mayavi import mlab, mayavi_plot_surfaces, SurfacePlot, mayavi_plot_surface

from gsurface.imodel import SurfaceGuidedInteractedMassSystems
from gsurface.imodel import *
from gsurface.forces.interaction import SpringInteraction, OneSideSpringInteraction

from gsurface.surface import Sphere, Tore, Plan

# objects
sphere = Sphere(1.0).translate(np.array([0.0, 0.0, 0.5]))
mesh_sphere = sphere.build_surface(*sphere.mesh(50, 50))

tore = Tore(r=0.5, R=2.0).translate(np.array([0.0, 0.0, 0.0]))
mesh_tore = tore.build_surface(*tore.mesh(50, 50))

plan_shift = np.array([0.0, 0.0, -0.6])
plan = Plan.from_xz_rotation(0.0).translate(plan_shift).setlims(v_ll=-3, v_ul=3, u_ll=-3, u_ul=3)
mesh_plan = plan.build_surface(*plan.mesh(50, 50))

gravity_vector = np.array([0.0, 0.0, -10.0])

# setup simulation for tore
tore_sim = SurfaceGuidedMassSystem(
    surface=tore,
    s0=build_s0(v0=np.pi/2, du0=1.0),
    m=1.0,
    forces=[
        # Gravity(1.0, np.array([0.0, 0.0, -9.0])),
        # ViscousFriction(0.5)
    ]
)

# setup simulation for sphere
sphere_sim = SurfaceGuidedMassSystem(
    surface=sphere,
    s0=build_s0(v0=np.pi/2),
    m=1.0,
    forces=[
        Gravity(1.0, gravity_vector),
        ViscousFriction(2.0)
    ]
)

plan_sim = SurfaceGuidedMassSystem(
    surface=plan,
    s0=build_s0(u0=2.0, v0=0.0),
    m=0.5,
    forces=[
        # Gravity(1.0, gravity_vector),
        # LengthedSpringForce(100.0, plan_shift, 0.7),
        ViscousFriction(200.0),
    ]
)

print(tore_sim)
print(sphere_sim)
print(plan_sim)

time = np.linspace(0.0, 10.0, 2000)

joint_sim = SurfaceGuidedInteractedMassSystems([tore_sim, sphere_sim, plan_sim], [
    OneSideSpringInteraction([tore_sim, sphere_sim], 0.25),
    OneSideSpringInteraction([tore_sim, plan_sim], 10),
])

# concept
# joint_sim.save("joint_sim_1.im")

# perf measurement
t1 = timelib.time()
data = joint_sim.solve(time, solver=solver.rk4)
t2 = timelib.time()

print(t2 - t1)

tore_solutions, sphere_solutions, plan_solutions = joint_sim.solutions(data, time)


# plot
animation = mayavi_plot_surfaces([
    SurfacePlot(mesh_sphere, trajectory=sphere_solutions[Tyi]),
    SurfacePlot(mesh_tore, trajectory=tore_solutions[Tyi], showSurface=True),
    SurfacePlot(mesh_plan, trajectory=plan_solutions[Tyi])
])

mlab.view(100, 72, 16, np.array([0.0,  0.0, 0.0]))

