import matplotlib.pyplot as plt
import numpy as np
from mayavi import mlab

from gsurface import SurfaceGuidedMassSystem, LengthedSpringForce, Gravity, ViscousFriction
from gsurface.indexes import Pi, Vi, nVi
from gsurface.surface.plan import Plan

# config

x0, vx0 = 1.0, -3.0

y0, v0 = 0.0, 0.0

# model

plan = Plan.from_xz_rotation(angle=0.0).setlims(-1, 1, -3, 1).multlims(1)

m = 1.0

system = SurfaceGuidedMassSystem(
    surface=plan,
    s0=np.array([x0, vx0, y0, v0]),
    m=m,
    forces=[
        Gravity(m=m, g=np.array([0.0, -1.0, 0.0])),
        LengthedSpringForce(stiffness=5.0, clip=np.array([0.0, 0.0, 0.0]), l0=1.0),
        LengthedSpringForce(stiffness=5.0, clip=np.array([0.0, -1.0, 0.0]), l0=1.0),
        ViscousFriction(mu=0.2),  # test for mu=0.2 and 0.8
    ]
)

# simulate
time = np.linspace(0, 40, 10000)

states = system.solve(time)

mesh = plan.build_surface(*plan.mesh(100, 100))

physics = system.solutions(states, time)

trajectory = physics[:, Pi]
speed = physics[:, Vi]
abs_speed = physics[:, nVi]


# plot surface & trajectory
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))

mlab.mesh(*mesh, opacity=1.0, colormap='binary')  # , color=(0.1, 0.1, 0.6)
mlab.mesh(*mesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')

mlab.points3d(*trajectory[0], color=(0, 0, 1), scale_factor=0.1)
mlab.points3d(0, 0, 0, color=(0, 1, 0), scale_factor=0.05)
mlab.points3d(0, -1, 0, color=(0, 1, 0), scale_factor=0.05)

mlab.plot3d(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0), tube_radius=0.01)

mlab.orientation_axes()

mlab.view(azimuth=-90, elevation=20)

# plot curves
plt.figure(2)

plt.subplot(2, 2, 1)
plt.plot(time, trajectory)
plt.title("Trajectory")
plt.xlabel("time (sec)")
plt.ylabel("position (m)")
plt.legend(["X", "Y", "Z"])
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(time, speed)
plt.title("Speed")
plt.xlabel("time (sec)")
plt.ylabel("speed (m/s)")
plt.legend(["Vx", "Vy", "Vz"])
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(time, abs_speed)
plt.title("Absolute speed")
plt.xlabel("time (sec)")
plt.ylabel("speed (m/s)")
plt.legend(["V"])
plt.grid(True)

# plt.subplot(2, 2, 2)
# plt.plot(time, force)
# plt.title("Debug Force")
# plt.xlabel("time (sec)")
# plt.ylabel("force (N)")
# plt.legend(["Fx", "Fy", "Fz"])
# plt.grid(True)

plt.show()