from __future__ import annotations

from .surface import Surface

import numpy as np


# todo definir le plan a partir de'angles de rotations autour des axes
# parameters are x = u, v = y
class Plan(Surface):

    __repr_str__ = "(a={a:.2f}, a={b:.2f})"

    @staticmethod
    def from_xz_rotation(angle: float = 0.0) -> Plan:
        return Plan(np.tan(angle), 0.0)

    def __init__(self, a: float = 1.0, b: float = 1.0):
        self.a = a
        self.b = b

    def eval(self, u: float, v: float):
        return self.buildevalreturn(
            x=u,
            y=v,
            z=self.a*u + self.b*v,

            dux=1,
            duz=self.a,

            dvy=1,
            dvz=self.b
        )