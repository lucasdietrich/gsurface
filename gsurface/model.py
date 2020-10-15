from ode.system import ODESystem

from .surface.surface import Surface

import numpy as np

from .indexes import *

from typing import Union, Iterable, Tuple

from .forces import Force, Gravity, ForceSum


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
        u, du, v, dv = s

        w = np.array([u, v])

        dw = np.array([du, dv])

        # eval
        # todo simplify/optimize eval
        S, J, H = self.surface.eval(u, v)

        # feed all interacted forces

        # eval force:
        F = self.forces.eval(w, dw, t, S, J)

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


class SurfaceGuidedFallMassSystem(SurfaceGuidedMassSystem):
    def __init__(self, surface: Surface, s0: np.ndarray = None, m: float = 1.0, g: np.ndarray = None):
        super(SurfaceGuidedFallMassSystem, self).__init__(
            surface, s0, m, Gravity(m, g)
        )