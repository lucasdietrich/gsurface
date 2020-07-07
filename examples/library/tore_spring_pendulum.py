from surface_guided_sim import SurfaceGuidedMassSystem, SpringForce, LengthedSpringForce, Gravity, AirFriction, ViscousFriction

from surface_guided_sim.surface import Tore

from surface_guided_sim.indexes import *

from surface_guided_sim.plotter import mayavi_plot_surface, matplotlib_plot_solutions, mayavi_animate_surface_trajectory

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
        ViscousFriction(mu=0.5),
    ]
)

# simulate
time = np.linspace(0, 10, 5000)

states = system.solve(time)

mesh = tore.mesh(100, 100)

smesh = tore.buildsurface(*mesh)

physics = system.solutions(states, time)

trajectory = physics[:, Si]
speed = physics[:, Vi]
abs_speed = physics[:, nVi]
force = physics[:, Fi]

# plot surface & trajectory
# mayavi_plot_surface(smesh, trajectory)

anim = mayavi_animate_surface_trajectory(smesh, trajectory[::3], abs_speed[::3])

# spring clip
mlab.points3d(0, 0, 0, color=(0, 1, 0), scale_factor=0.05)

mlab.view(azimuth=-90, elevation=20)

anim()



# plot curves
matplotlib_plot_solutions(time, physics, system)

plt.show()