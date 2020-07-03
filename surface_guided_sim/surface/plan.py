from __future__ import annotations

from .surface import Surface

import numpy as np


# todo definir le plan a partir de'angles de rotations autour des axes
# parameters are x = u, v = y
class Plan(Surface):

    @staticmethod
    def from_xz_rotation(angle: float = 0.0) -> Plan:
        return Plan(np.tan(angle), 0.0)

    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def eval(self, u: float, v: float):

        x = u
        y = v
        z = self.a*u + self.b*v

        dux = 1
        duy = 0
        duz = self.a

        dvx = 0
        dvy = 1
        dvz = self.b

        duux = 0
        duuy = 0
        duuz = 0

        duvx = 0
        duvy = 0
        duvz = 0

        dvvx = 0
        dvvy = 0
        dvvz = 0

        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])