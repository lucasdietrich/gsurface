from __future__ import annotations

from .surface import Surface, SJH

import numpy as np


# cette définition du plan ne peux pas être parallele à l'axe Z
# todo definir le plan a partir d'angles de rotations autour des axes
# parameters are x = u, v = y
class Plan(Surface):

    __repr_str__ = "(a={a:.2f}, a={b:.2f})"

    @staticmethod
    def from_xz_rotation(angle: float = 0.0) -> Plan:
        return Plan(np.tan(angle), 0.0)

    def __init__(self, a: float = 1.0, b: float = 1.0):
        self.a = a
        self.b = b

    def _definition(self, u: float, v: float) -> SJH:
        # rather than using buildMetric, we can build S, J and H manually
        S = np.array([u, v, self.a*u + self.b*v])
        J = np.array([
            [1, 0],
            [0, 1],
            [self.a, self.b]
        ])
        H = np.zeros((3, 2, 2))

        return S, J, H
