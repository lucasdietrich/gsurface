# high layer - synthetic layer

from typing import Union

from gsurface import SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems

Model = Union[SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems]


class Solver:
    def __init__(self, model: Model):
        pass