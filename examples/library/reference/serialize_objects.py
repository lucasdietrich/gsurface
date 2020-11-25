# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable

import numpy as np

from gsurface import SurfaceGuidedMassSystem
from gsurface.advanced.structure import TriangleStructure, SurfaceGuidedStructureSystem, Solid
from gsurface.forces import StaticFieldElectroMagneticForce, SpringForce, ViscousFriction, Gravity, DistanceGravity
from gsurface.serialize import save, load, saveB64, loadB64
from gsurface.surface import Plan, Tore, Sphere, Catenoid

filename = "_tmp/serialized_plan.txt"

plan = Plan(1, 2, 3, 1)
plan.translate(np.array([1.0, 2.0, 0.0]))

sphere = Sphere().multlims(2).translate(np.array([1.0, 2.0, 0.0]))
tore = Tore()
cat = Catenoid()

forces = [
    StaticFieldElectroMagneticForce(1.0, np.array([1.0, 2.0, 3.0])),
    SpringForce(),
    ViscousFriction(),
    Gravity(),
    Gravity() + DistanceGravity()
]

model1 = SurfaceGuidedMassSystem(
    surface=sphere,
    forces=forces
)

structure = TriangleStructure(23.0, 1.0, 23.0, 4.3)
structure[0, 2].mu = 2.0
structure[0, 1].mu = 3.0
structure[1, 2].mu = 4.0
model2 = SurfaceGuidedStructureSystem(
    sphere, structure, forces
)

objects = [(plan, structure, forces, model1, Solid()) for i in range(100)]
objects = sphere

# print(surfaces)
save(filename, objects, 4)
saveB64(filename + "b64", objects)

obj = load(filename)
obj2 = loadB64(filename + "b64")
