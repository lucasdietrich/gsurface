from surface_guided_sim import SurfaceGuidedMassSystem, SpringForce, LengthedSpringForce, Gravity, AirFriction, ViscousFriction

from surface_guided_sim.surface import Tore

from surface_guided_sim.indexes import *

from surface_guided_sim.plotter import mayavi_plot_surface, matplotlib_plot_solutions

import matplotlib.pyplot as plt
from mayavi import mlab

import numpy as np

# config

u0, du0 = 0.0, 0.5

v0, dv0 = 1.0, 0.0

# model

tore = Tore(0.5, 1.0)

m = 1.0

system = SurfaceGuidedMassSystem(
    surface=tore,
    s0=np.array([u0, du0, v0, dv0]),
    m=m,
    forces=[
        SpringForce(stiffness=5.0, clip=np.array([0.0, 0.0, 0.0])),
        # LengthedSpringForce(stiffness=5.0, clip=np.array([0.0, 0.0, 0.0]), l0=1.0),
        ViscousFriction(mu=0.4),
    ]
)

# simulate
time = np.linspace(0, 20, 5000)

states = system.solve(time)

mesh = tore.buildsurface(*tore.mesh(100, 100))

physics = system.solutions(states, time)

trajectory = physics[:, Si]
speed = physics[:, Vi]
abs_speed = physics[:, nVi]
force = physics[:, Fi]

# plot surface & trajectory
mayavi_plot_surface(mesh, trajectory)

# spring clip
mlab.points3d(0, 0, 0, color=(0, 1, 0), scale_factor=0.05)

mlab.view(azimuth=-90, elevation=20)

# plot curves
matplotlib_plot_solutions(time, physics, system)

plt.show()