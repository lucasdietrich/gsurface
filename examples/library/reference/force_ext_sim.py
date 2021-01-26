# Simulating Solid tied to (0, 0, 0) with a lengthed spring + viscous friction + gravity

import numpy as np
from scipy.integrate import odeint

from gsurface.forces import Gravity, ViscousFriction, LengthedSpringForce
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot

mass: float = 1.0  # kg

forces = Gravity(mass) + ViscousFriction(mu=0.2) + LengthedSpringForce(stiffness=100.0, l0=0.5)


def ds(S: np.ndarray, t: float):
    dS = np.zeros_like(S)

    X = S[::2]
    V = S[1::2]

    dS[0::2] = V
    dS[1::2] = forces.eval(t, X, V) / mass

    return dS


s0 = np.array([
    0.0, 0.0, 0.0, 0.0, -0.5, 0.0  # x, vx, y, vy, z, vz
])

time = np.linspace(0, 5, 1000)

states = odeint(ds, s0, time)

mayavi_plot_surfaces([
    SurfacePlot(trajectory=states[:, ::2], animate=True)
])

