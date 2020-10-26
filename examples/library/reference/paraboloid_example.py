from gsurface.surface import EllipticParaboloid, HyperbolicParaboloid
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.forces import Gravity, ViscousFriction, SpringForce, LengthedSpringForce
from gsurface import Tyi, Emi
from gsurface.plotter.matplotlib import matplotlib_plot_solutions

import numpy as np

# choose
surface_class = EllipticParaboloid  # or EllipticParaboloid

if surface_class is HyperbolicParaboloid:
    para = HyperbolicParaboloid(1.0, 5).setlims(v_ul=10)
    s0 = build_s0(u0=0.0, v0=1.0, du0=3)
else:
    para = EllipticParaboloid(1.0, 1.0)
    s0 = build_s0(u0=0.0, v0=1.0, du0=2)

surface = para.build_surface(*para.mesh(50, 50))

print(para, para.check(20, 20))

model = SurfaceGuidedMassSystem(
    surface=para,
    s0=s0,
    m=1.0,
    forces=[
        Gravity(m=1.0, g=np.array([0.0, 0.0, -2])),
        ViscousFriction(mu=0.5)
    ]
)

time = np.linspace(0, 20, 2000)

data = model.solve(time)

solutions = model.solutions(data, time)

trajectory = solutions[Tyi]

matplotlib_plot_solutions(time, data, solutions)

mayavi_plot_surfaces([
    SurfacePlot(surface, trajectory=trajectory, animate=True)
])

mlab.view(0, 30, 5.0, np.zeros((3,)))
