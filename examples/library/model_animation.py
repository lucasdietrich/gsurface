from surface_guided_sim import SurfaceGuidedMassSystem, SpringForce, LengthedSpringForce, Gravity, \
    AirFriction, ViscousFriction, build_s0

from surface_guided_sim.surface import Tore, Sphere, Plan, EggBox, ConicalCorner, Catenoid

from surface_guided_sim.indexes import *

from surface_guided_sim.plotter import matplotlib_plot_solutions, mayavi_animate_surface_trajectory

from mayavi import mlab

import numpy as np

m = 1.0
systems = [
    SurfaceGuidedMassSystem(
        surface=Tore(0.5, 1.0),
        s0=build_s0(u0=0.0, du0=0.5, v0=1.0, dv0=0.0),
        m=m,
        forces=[
            SpringForce(stiffness=5.0, clip=np.array([0.0, 0.0, 0.0])),
            Gravity(m=m, g=np.array([0.0, 0.0, -2.0])),
            LengthedSpringForce(stiffness=5.0, clip=np.array([1.0, 1.0, 0.0]), l0=1.0),
            ViscousFriction(mu=0.5),
        ]
    ),
    SurfaceGuidedMassSystem(
        surface=Sphere(1.0),
        s0=build_s0(u0=0.0, du0=1.0, v0=np.pi/2, dv0=5.0),
        m=m,
        forces=[
            ViscousFriction(mu=0.5),
            Gravity(m=m, g=np.array([0.0, -1.0, 0.0])),
            LengthedSpringForce(stiffness=15.0, clip=np.array([0.0, 2.0, 0.0]), l0=2)
        ]
    ),
    SurfaceGuidedMassSystem(
        surface=Tore(0.5, 2.0),
        s0=build_s0(u0=0.0, du0=2, v0=0.0, dv0=40.0),
        m=m,
        forces=[
            ViscousFriction(mu=0.5),
            Gravity(m=m, g=np.array([0.0, -3.0, 0.0])),
        ]
    ),
    SurfaceGuidedMassSystem(
        surface=Catenoid().multlims(1.5),
        s0=build_s0(du0=0.02, dv0=2),
        m=m,
        forces=[

        ]
    )
]

system = systems[3]

# simulate
time = np.linspace(0, 7, 20000)

states = system.solve(time)

mesh = system.surface.mesh(100, 100)

smesh = system.surface.buildsurface(*mesh)

physics = system.solutions(states, time)

trajectory = physics[:, Si]
speed = physics[:, Vi]
abs_speed = physics[:, nVi]
force = physics[:, Fi]

matplotlib_plot_solutions(time, states, physics)

anim = mayavi_animate_surface_trajectory(smesh, trajectory[::3], abs_speed[::3])

# spring clip
mlab.points3d(0, 0, 0, color=(0, 1, 0), scale_factor=0.05)

mlab.view(azimuth=-90, elevation=20)

anim()

mlab.show()