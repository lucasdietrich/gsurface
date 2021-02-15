from .model import SurfaceGuidedStructureSystem, ForcesType
from .posgraph import ExplStructureGraph
from gsurface.surface.plan import Plan
from . import Solid

import numpy as np


class PlanExplStructureSystem(SurfaceGuidedStructureSystem):
    def __init__(self, expl_structure: ExplStructureGraph, v0: np.ndarray = None, structureForces: ForcesType = None, **kargs):
        super(PlanExplStructureSystem, self).__init__(
            Plan(1.0, 0.0, 0.0, 0.0),
            structure=expl_structure,
            s0=None,
            structureForces=structureForces
        )

        if v0 is None:
            v0 = np.zeros((expl_structure.N*2))

        self.s0[1::2] = v0
