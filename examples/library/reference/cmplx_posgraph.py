import pprint

import numpy as np

from gsurface.advanced.structure import ExplStructureGraph, Solid

from gsurface.advanced.structure.pmodel import PlanExplStructureSystem

from gsurface.serialize import save_attached

N = 7

structure = ExplStructureGraph(
    nodes=[Solid() for i in range(N)],
    positions=[np.array([i, i % 2, i % 3]) for i in range(N)]
)

model = PlanExplStructureSystem(structure)

pprint.pprint(structure.interactions)

ext_imodel = save_attached(model, __file__ + ".imodel")
ext_struct = save_attached(structure, __file__ + ".structure")