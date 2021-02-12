import numpy as np

from gsurface.forces import Gravity, ViscousFriction, SpringForce, LengthedSpringForce
from gsurface.model import SurfaceGuidedMassSystem, build_s0
from gsurface.advanced.structure import SurfaceGuidedStructureSystem, TriangleStructure, BowStructure, CarStructure, SnakeStructure
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
        Gravity(1.0, np.array([0.0, 0.0, 9.0])),
        ViscousFriction(0.5)
    ]
)


tore_sim2 = SurfaceGuidedMassSystem(
    surface=Tore(0.5, 1.0),
    s0=build_s0(u0=0.0, du0=0.5, v0=1.0, dv0=0.0),
    m=1.0,
    forces=[
        SpringForce(stiffness=5.0, clip=np.array([0.0, 0.0, 0.0])),
        Gravity(m=1.0, g=np.array([0.0, 0.0, -2.0])),
        LengthedSpringForce(stiffness=5.0, clip=np.array([1.0, 1.0, 0.0]), l0=1.0),
        ViscousFriction(mu=0.5),
    ]
)


model_structure = SurfaceGuidedStructureSystem(surface=Tore(),
                                               structure=TriangleStructure(totalMass=4.0, stiffness=1000.0, mu=10.0,
                                                                           l0=0.5), structureForces=[
        Gravity(1.0, np.array([0.0, 0.0, -9.81])),
        ViscousFriction(1.0)
    ])

model_structure.s0 = np.array([ 4.73114640e-01,  5.00000000e+00,  2.81624913e-02,  2.50000000e+01,
       -1.60399682e-02,  0.00000000e+00, -2.36683950e-01,  0.00000000e+00,
       -1.20742294e-01,  0.00000000e+00,  3.40214807e-01,  0.00000000e+00])
