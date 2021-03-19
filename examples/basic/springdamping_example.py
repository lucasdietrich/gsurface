import numpy as np

from gsurface import Plan, SurfaceGuidedMassSystem, build_s0
from gsurface.forces import CenterDirectedViscousFriction, ConstantDirectedViscousFriction
from gsurface.forces import SpringDampingForce
from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot, Tyi

# simulate a 2D spring damping system, we notice that the radial speed tends to 0 where rotational speed still constant

plan = Plan(a=0.0, c=1.0)
surface = plan.build_surface(*plan.mesh(50, 50))

model = SurfaceGuidedMassSystem(
    surface=plan,
    s0=build_s0(u0=0.5, du0=0.0, dv0=5),
    m=1.0,
    forces=[
        ConstantDirectedViscousFriction(1.0, np.array([1.0, 0.0, 0.0])),
        CenterDirectedViscousFriction(1.0),
        SpringDampingForce(100.0, 1.0, None, 1.0)
    ]
)

time = np.linspace(0, 10, 3000)

data = model.solve(time)

solutions = model.solutions(data, time)

mayavi_plot_surfaces([
    SurfacePlot(surface, trajectory=solutions[Tyi])
])

from gsurface.serialize import save_attached
model_parsed = save_attached(model, __file__)