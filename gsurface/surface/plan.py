from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation

from .surface import Surface, SJH


# https://fr.wikipedia.org/wiki/Plan_(math%C3%A9matiques)
# http://www.easy-math.net/transforming-between-plane-forms/
class Plan(Surface):
    __repr_str__ = " Norm a, b, c = {a:.2f}, {b:.2f}, {c:.2f}, d = {d:.2f}"

    # cartesian definition of plan
    def __init__(self, a: float = 1.0, b: float = 0.0, c: float = 0.0, d: float = 0.0, **kargs):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        # build norm vector
        self.n = np.array([a, b, c])

        # eval norm
        self.norm = np.linalg.norm(self.n)

        # check if plan is well defined
        if not any(self.n):
            raise Exception("Wrong plan definition : normal vector to plan cannot be null")

        # build orthogonal vector to n
        if self.a == 0:
            self.nT = np.array([0, c, -b])
        else:
            self.nT = np.array([b, -a, 0])

        # build U, Un
        self.U = self.nT
        self.Un = self.U / np.linalg.norm(self.U)

        # build V, Vn
        self.V = np.cross(self.n, self.nT)
        self.Vn = self.V / np.linalg.norm(self.V)

        # build shift
        self.D = d * self.n / self.norm

        # build J and H

        self.J = np.array([self.Un.T, self.Vn.T]).T
        self.H = np.zeros((3, 2, 2))
        
        super(Plan, self).__init__()

    def evalS(self, u: float, v: float) -> np.ndarray:
        return self.D + u * self.Un + v * self.Vn

    def _definition(self, u: float, v: float) -> SJH:
        return self.evalS(u, v), self.J, self.H

    # must always give 0
    def utest(self, u: float, v: float):
        return np.dot(self.evalS(u, v), self.n) - self.d

    # base vector n = [1, 0, 0]
    # rotation around y or around z
    @staticmethod
    def from_rotations(alpha: float = 0.0, theta: float = 0.0, shift: float = 0.0) -> Plan:
        rot = Rotation.from_rotvec([0.0, alpha, theta]).as_matrix()

        nx = np.array([1.0, 0.0, 0.0])

        n = nx @ rot.T

        return Plan(*n, d=shift)

    # retrocompatibility
    @staticmethod
    def from_xz_rotation(angle: float = 0.0) -> Plan:
        return Plan.from_rotations(angle - np.pi / 2, 0.0, 0.0)
