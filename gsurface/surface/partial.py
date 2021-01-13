from __future__ import annotations

from .surface import Surface, SJH

from abc import abstractmethod, ABC


class PartialSurface(Surface, ABC):
    @staticmethod
    def buildMetric(
            x=0.0, y=0.0, z=0.0,
            dux=0.0, dvx=0.0, duy=0.0,
            dvy=0.0, duz=0.0, dvz=0.0,
            duux=0.0, duvx=0.0, dvvx=0.0,
            duuy=0.0, duvy=0.0, dvvy=0.0,
            duuz=0.0, duvz=0.0, dvvz=0.0
    ) -> SJH:
        return Surface.buildMetric(x, y, z, *([0]*12))



    def check(self, nu: int = 20, nv: int = 20, tolerance=1e-7):
        return NotImplementedError("PartialSurface does not define derivatives")

    def check_verbose(self, nu: int = 20, nv: int = 20, tolerance=1e-7):
        return NotImplementedError("PartialSurface does not define derivatives")

