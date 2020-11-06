# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable

import numpy as np

import json

from gsurface.misc.json import GSurfaceEncoder, GSurfaceDecoder

from gsurface.surface import Plan, Tore, Sphere, Catenoid
from gsurface.forces import StaticFieldElectroMagneticForce, SpringForce, ViscousFriction, Gravity, DistanceGravity
from gsurface import SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems

from gsurface.advanced.structure import TriangleStructure, SurfaceGuidedStructureSystem, StructureGraph, SolidParameters, InteractionParameters

filename = "_tmp/serialized_plan.txt"

plan = Plan(1, 2, 3, 1)
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

structure = StructureGraph([
    SolidParameters(),
    SolidParameters()
],
interactions={
    (0, 1): InteractionParameters()
})
model2 = SurfaceGuidedStructureSystem(
    sphere, structure, forces
)

save = structure, forces, model1, SolidParameters()

# print(surfaces)

with open(filename, "w+") as fp:
    json.dump(save, fp, cls=GSurfaceEncoder, indent=2)

with open(filename, "r+") as fp:
    obj = json.load(fp, cls=GSurfaceDecoder)

# print(obj)