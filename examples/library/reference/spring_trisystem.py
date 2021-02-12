from gsurface.surface import Tore, EggBox
from gsurface.forces import SpringInteraction, Gravity, ViscousFriction
from gsurface.plotter import mayavi_plot_surfaces, matplotlib_plot_solutions, SurfacePlot
from gsurface import SurfaceGuidedInteractedMassSystems, SurfaceGuidedMassSystem, Tyi, build_s0

import numpy as np

# queue of N solids, attached with a spring

SYSTEMS = 8

stiffness = 10

tore = Tore(0.5, 1.0)
tore_mesh = tore.build_surface(*tore.mesh(50, 50))

# build model
joint_sim = SurfaceGuidedInteractedMassSystems(
    [
        SurfaceGuidedMassSystem(
            surface=tore,
            s0=build_s0(0, 2*j, 0.0, 1+j),
            m=1.0,
            forces=[
                ViscousFriction(0.2),
                Gravity(1.0, np.array([0.0, 0.0, -1.0]))
            ]
        ) for j in range(SYSTEMS)
    ],
    {
        (i, i + 1): SpringInteraction(1.0) for i in range(SYSTEMS - 1)
    }
)

time = np.linspace(0, 25, 2000)

data = joint_sim.solve(time)

solutions = joint_sim.solutions(data, time)

colors = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 1, 1)
]

NCOLORS = len(colors)

mayavi_plot_surfaces([
    SurfacePlot(
        tore_mesh,  # surface
        i == 0,
        trajectory=solution[Tyi],
        trajectoryColor=colors[i % NCOLORS],
        showTrajectory=True
    ) for i, solution in enumerate(solutions)
])
