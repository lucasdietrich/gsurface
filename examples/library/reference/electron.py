# todo fix
# inspiration : http://www.chimix.com/an9/sup9/pharm11.htm#:~:text=Les%20%C3%A9lectrons%20sont%20soumis%20%C3%A0,en%20S%20et%20en%20O.

from gsurface.surface import Plan
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.forces import StaticFieldElectroMagneticForce
from gsurface.indexes import Eki, Epi, Emi, Si, Fi, Tyi
from gsurface.plotter.matplotlib import matplotlib_plot_solutions
from gsurface.plotter.mayavi import mayavi_plot_surfaces, SurfacePlot

import numpy as np

import matplotlib.pyplot as plt

plan = Plan(1.0)
surface = plan.build_surface(*plan.mesh(50, 50))

d = 10.0e-2  # cm
U = 5.0e3    # V

# electron
#  https://fr.wikipedia.org/wiki/%C3%89lectron
me = 9.109e-31  # kg
qe = -1.602e-19  # C

# proton
#  https://fr.wikipedia.org/wiki/Proton
mp = 1.672e-27  # kg
qp = -qe  # C

E = np.array([0.0, U / d, 0.0])   # V/m
B = np.array([0.0, 0.0, 8.0e-2])  # T

model = SurfaceGuidedMassSystem(
    surface=plan,
    s0=build_s0(u0=0.0, du0=2.0e6),
    m=mp,
    forces=[
        StaticFieldElectroMagneticForce(
            q=qp,
            E=E,
            B=None,
        ),
    ]
)

T = np.linspace(0.0, 1.0e-4, 1000)

states = model.solve(T)

solutions = model.solutions(states, T)

plt.figure(1)
plt.plot(T, solutions[:, 1])
plt.grid(True)
plt.show()

# mayavi_plot_surfaces([
#     SurfacePlot(surface)
# ])

