# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable

import numpy as np
from scipy.spatial.transform import Rotation

from gsurface import SurfaceGuidedMassSystem, build_s0
from gsurface.advanced.structure import TriangleStructure, SurfaceGuidedStructureSystem
from gsurface.forces import StaticFieldElectroMagneticForce, SpringForce, ViscousFriction, Gravity, NewtonGravity
from gsurface.serialize import save, load
from gsurface.surface import Plan, Tore, Sphere, Catenoid

filename = "_tmp/serialized_plan.txt"

plan = Plan(1, 2, 3, 1)
plan.translate(np.array([1.0, 2.0, 0.0]))

sphere = Sphere(0.5).multlims(0.5).translate(np.array([1.0, 2.0, 0.0])).rotate(Rotation.from_rotvec([0.0, 1.0, 2.0]).as_matrix())
tore = Tore()
cat = Catenoid()

forces = [
    StaticFieldElectroMagneticForce(1.0, np.array([1.0, 2.0, 3.0])),
    SpringForce(),
    ViscousFriction(),
    Gravity(),
    Gravity() + NewtonGravity()
]

model1 = SurfaceGuidedMassSystem(
    surface=sphere,
    forces=forces,
    solid=23.0,
    s0=build_s0(1.0, 2.0, 3.0, 4.0)
)

structure = TriangleStructure(23.0, 1.0, 23.0, 4.3)
structure[0, 2].mu = 2.0
structure[0, 1].mu = 3.0
structure[1, 2].mu = 4.0
model2 = SurfaceGuidedStructureSystem(
    sphere, structure, forces
)

objects = model1

# print(surfaces)
save(filename, objects, 4)
# saveB64(filename + "b64", objects)

obj = load(filename)
# obj2 = loadB64(filename + "b64")

save(filename + ".2.txt", obj, 4)

# compare files
