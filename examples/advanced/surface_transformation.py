import numpy as np
from scipy.spatial.transform import Rotation

from gsurface.forces import Gravity, ViscousFriction, SpringDampingForce
from gsurface.model import SurfaceGuidedMassSystem, build_s0, Tyi
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, mlab
from gsurface.surface import Plan

angle = 0.1*np.pi/2  # np.pi/2

plan = Plan(1.0, 0.0, 0.0).rotate(Rotation.from_rotvec(np.array([np.pi, 0.0, 0.0])).as_matrix())
# plan = Plan.from_rotations(0.0, np.pi, 0.0) # equivalent définition

plan.shiftvector = np.array([0.0, 0.0, 1.0])

surface = plan.build_surface(*plan.mesh(50, 50))

model = SurfaceGuidedMassSystem(
        surface=plan,
        s0=build_s0(0.5, 0.0, 0.0, 0.0),
        m=1.0,
        forces=[
            Gravity(m=1.0, g=np.array([0.0, 0.0, -10.0])),
            SpringDampingForce(stiffness=1000.0, mu=10.0, clip=np.array([0.0, 0.0, 0.0]), l0=0.5),
            ViscousFriction(mu=0.5)
        ]
    )


time = np.linspace(0, 10, 1000)

states = model.solve(time)
solutions = model.solutions(states, time)

mayavi_plot_surfaces([
    SurfacePlot(surface, trajectory=solutions[Tyi]),
])

mlab.points3d(0.0, 0.0, 0.0, color=(0, 1, 0), scale_factor=0.05)
mlab.view(0, 90, 6.0, [0.0, 0.0, 0.0])