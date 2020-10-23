import numpy as np

from gsurface.forces import Gravity, ViscousFriction
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.surface import Sphere, Tore

# setup simulation for tore
tore = Tore(r=0.5, R=1.0).translate(np.array([3.0, 0.0, 0.0]))

tore_sim = SurfaceGuidedMassSystem(
    surface=tore,
    s0=build_s0(du0=10.0),
    m=1.0,
    forces=[
        Gravity(1.0, np.array([0.0, 0.0, -9.0])),
        ViscousFriction(0.5)
    ]
)

# setup simulation for sphere
sphere = Sphere(1.0)

sphere_sim = SurfaceGuidedMassSystem(
    surface=sphere,
    s0=build_s0(u0=1.5, du0=10.0, v0=1.5),
    m=1.0,
    forces=[
        Gravity(1.0, np.array([0.0, 0.0, +9.0])),
        ViscousFriction(0.5)
    ]
)
