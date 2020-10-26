from typing import Union, Iterable

import numpy as np
from ode.system import ODESystem

from .forces import Force, Gravity, ForceSum
from .indexes import *
from .surface.surface import Surface

from gsurface.types import ModelEvalState


def build_s0(u0: float = 0.0, du0: float = 0.0, v0: float = 0.0, dv0: float = 0.0):
    return np.array([u0, du0, v0, dv0])


class SurfaceGuidedMassSystem(ODESystem):
    def __init__(
            self, surface: Surface,
            s0: np.ndarray = None,
            m: float = 1.0,
            forces: Union[Force, ForceSum, Iterable[Force]] = None
    ):
        self.surface: Surface = surface

        self.forces: ForceSum = ForceSum(forces)

        if s0 is None:
            s0 = build_s0()

        self.m = m

        super(SurfaceGuidedMassSystem, self).__init__(s0)

    def __repr__(self):
        return f"{self.__class__.__name__} for solid of mass={self.m}kg on surface {self.surface} " \
               f"with s0 = {self.s0}\n" \
               f"and forces : {self.forces}"

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        """
        Deriv function

        :param s:
        :param t:
        :return:
        """
        M = ModelEvalState()

        # vars
        w = M.w = s[::2]
        M.dw = s[1::2]

        # todo simplify/optimize eval
        M.S, M.J, M.H = self.surface.eval(*w)

        # feed all interacted forces

        # eval force:
        F = self.forces.evalM(t, M)

        # eval and return
        return self.dsM(F, M)

    def dsM(self, F: np.ndarray, M: ModelEvalState):
        return self.ds(M.dw, F, M.J, M.H)

    def ds(self, dw: np.ndarray, F: np.ndarray, J: np.ndarray, H: np.ndarray) -> np.ndarray:
        """
        Eval ds for position and speed (w, dw) from calculated forces (F) and surface (S, J, H)

        :param w:
        :param dw:
        :param F:
        :param S:
        :param J:
        :param H:
        :return:
        """
        # vars
        du, dv = dw

        # build intermediate symbols
        Duu, Dvv = np.sum(J**2, axis=0)

        Puv = np.vdot(J[:, ui], J[:, vi])

        wHw = dw.T @ H @ dw

        G = wHw - F / self.m

        Ru, Rv = np.dot(G, J)

        D = Duu * Dvv - Puv**2

        # build derivative state
        ds = np.array([
            # u
            du,
            (Rv * Puv - Ru * Dvv) / D,

            # v
            dv,
            (Ru * Puv - Rv * Duu) / D
        ])

        return ds

    def solutions(self, states: np.ndarray, time: np.ndarray):
        assert states.shape[0] == time.shape[0]

        physics = np.zeros((states.shape[0], 14))

        for i, (s, t) in enumerate(zip(states, time)):

            w = s[0::2]
            dw = s[1::2]

            S, J, H = self.surface.eval(*w)

            F = self.forces.eval(w, dw, t, S, J)

            V = J @ dw.T
            normV = np.linalg.norm(V, 2)

            Ek = 0.5 * self.m * normV**2
            Ep = np.sum(force.potential(t, S) for force in self.forces.get_conservative_forces())
            Em = Ek + Ep

            physics[i] = np.concatenate([
                S,
                V,
                F,
                [
                    normV,
                    np.linalg.norm(F, 2),
                    Ek,
                    Ep,
                    Em,
                ]
            ])

        return physics

    def export(self):
        raise NotImplementedError
