"""

This example shows how to use Forces in a simple ODE model.

A solid (mass 1kg) is subjected to gravity, viscous friction and a spring of length l0=0.5m

"""

import numpy as np
from scipy.integrate import odeint

from gsurface.forces import Gravity, ViscousFriction, LengthedSpringForce
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab

mass: float = 1.0  # kg

forces = Gravity(mass) + LengthedSpringForce(stiffness=100.0, l0=0.5) + ViscousFriction(mu=0.05)


# ODE model
def ds(S: np.ndarray, t: float):
    dS = np.zeros_like(S)

    X = S[::2]
    V = S[1::2]

    dS[0::2] = V
    dS[1::2] = forces.eval(t, X, V) / mass

    return dS


# initial state
s0 = np.array([
    0.1, 0.2, 0.0, 1.5, 0.0, 0.0  # x, vx, y, vy, z, vz
])

time = np.linspace(0, 10, 2000)

states = odeint(ds, s0, time)

mayavi_plot_surfaces([
    SurfacePlot(trajectory=states[:, ::2], animate=True)
])

mlab.view(0.0, 90.0, 5.0)
