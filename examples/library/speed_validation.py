from surface_guided_sim import SurfaceGuidedMassSystem, SpringForce, LengthedSpringForce, Gravity, AirFriction, ViscousFriction
from surface_guided_sim.indexes import *

from surface_guided_sim.surface import Sphere, Plan, Tore

import matplotlib.pyplot as plt
from mayavi import mlab

import numpy as np

# model

sphere = Sphere(1.0)

m = 1.0
g = np.array([-1.0, 0.0, 0.0])
k = 1.0
clip = np.array([0.0, 0.0, 1.0])

system = SurfaceGuidedMassSystem(
    surface=sphere,
    s0=np.array([np.pi/2, 1.0, np.pi/2, 0.0]),
    m=m,
    forces=[
        Gravity(m=m, g=g),
        SpringForce(stiffness=k, clip=clip),
        # ViscousFriction(mu=0.2),
    ]
)

# simulate
time = np.linspace(0, 20, 5000)

states = system.solve(time)

# build (todo opti)
mesh = sphere.buildsurface(*sphere.mesh(50, 50))

physics = system.solutions(states, time)

trajectory = physics[:, Si]
speed = physics[:, Vi]
abs_speed = physics[:, nVi]

Ec = 0.5 * m * abs_speed**2

Epk = np.zeros_like(Ec)
for i in range(len(trajectory)):
    Epk[i] = 0.5*k*np.linalg.norm(trajectory[i] - clip, 2)**2

Epg = - m*trajectory.dot(g)

Ep = Epg + Epk
Em = Ec + Ep


# plot surface & trajectory
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))

mlab.mesh(*mesh, opacity=0.3, colormap='cool')  # , color=(0.1, 0.1, 0.6)
mlab.mesh(*mesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')

mlab.points3d(*trajectory[0], color=(0, 0, 1), scale_factor=0.05)

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

plt.subplot(2, 2, 3)
plt.plot(time, abs_speed)
plt.title("Absolute speed")
plt.xlabel("time (sec)")
plt.ylabel("speed (m/s)")
plt.legend(["V"])
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(time, Ec)
plt.plot(time, Ep)
plt.plot(time, Em)
plt.title("Energies")
plt.xlabel("time (sec)")
plt.ylabel("energy (J)")
plt.legend(["Ec", "Ep", "Em"])
plt.grid(True)

plt.show()