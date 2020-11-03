import numpy as np

from gsurface.surface import Surface, SJH


class NewSurface(Surface):
    plimits = np.array([
        [-2.0, 2.0],
        [-2.0, 2.0]
    ])

    def _definition(self, u: float, v: float) -> SJH:
        return self.buildMetric(
            x=u - np.cos(v),
            y=v * np.sin(u) + v,
            z=np.sin(u - v) * u - v,

            dux=1,
            duy=v * np.cos(u),
            duz=u * np.cos(u - v) + np.sin(u - v),

            dvx=np.sin(v),
            dvy=np.sin(u) + 1,
            dvz=-u * np.cos(u - v) - 1,

            dvvx=np.cos(v),

            duuy=-v * np.sin(u),
            duvy=np.cos(u),

            duuz=-u * np.sin(u - v) + 2 * np.cos(u - v),
            duvz=u * np.sin(u - v) - np.cos(u - v),
            dvvz=-u * np.sin(u - v),
        )


surface = NewSurface().multlims(1.5)

surface.check_verbose(20, 20)

from gsurface import SurfaceGuidedMassSystem, Tyi, build_s0
from gsurface.forces import ViscousFriction, SpringForce

model = SurfaceGuidedMassSystem(
    surface=surface,
    s0=build_s0(u0=2.5, du0=-8.0, dv0=5.0),
    m=1.0,
    forces=[
        SpringForce(10.0),
        ViscousFriction(1.0)
    ]
)

from gsurface.plotter import mayavi_plot_surfaces, SurfacePlot

surface = NewSurface()

surface_mesh = surface.build_surface(*surface.mesh(50, 50))

time = np.linspace(0, 10, 1000)

data = model.solve(time)

solutions = model.solutions(data, time)

mayavi_plot_surfaces([
    SurfacePlot(surface_mesh, trajectory=solutions[Tyi])
])

