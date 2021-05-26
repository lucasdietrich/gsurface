import numpy as np

from gsurface import SurfaceGuidedMassSystem, build_s0
from gsurface.forces import Gravity, SpringForce, ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, Tyi
from gsurface.surface import Cylinder

mass = 1.0  # kg

system = SurfaceGuidedMassSystem(
    surface=Cylinder(R=1.0).setlims(v_ll=-1, v_ul=1),
    solid=mass,
    forces=Gravity(mass, g=np.array([0.0, 0.0, -1.0])) + SpringForce(stiffness=1.0, clip=np.array([-0.5, 0.0, 0.0])) + ViscousFriction(0.1),
    s0=build_s0(0, 0.5, 0, 0),
)

time = np.linspace(0, 50.0, 1000)

data = system.solve(time)

solutions = system.solutions(data, time)

smesh = system.surface.build_surface(*system.surface.mesh(40, 40))

mayavi_plot_surfaces([
    SurfacePlot(smesh, showSurface=True, trajectory=solutions[Tyi])
])
