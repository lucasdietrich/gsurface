from ode.system import ODESystem

from .surface.surface import Surface

import numpy as np

from .indexes import *

from typing import Union, Iterable

from .forces import Force, Gravity, ForceSum


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
            s0 = np.array([
                0.0,  # u
                0.0,  # vu
                0.0,  # v
                0.0,  # vu
            ])

        self.m = m

        super(SurfaceGuidedMassSystem, self).__init__(s0)

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        u, du, v, dv = s

        w = np.array([u, v])

        dw = np.array([du, dv])

        # eval
        eval, S, J, H = self.surface.SJH(u, v)

        # eval force:
        F = self.forces.eval(w, dw, t, S, J)

        # build intermediate symbols
        Duu, Dvv = np.sum(J**2, axis=0)

        # build common mult
        Puv = np.vdot(J[:, ui], J[:, vi])

        wHw = dw.T @ H @ dw

        # build residual
        Ru, Rv = np.dot(wHw - F, J) / self.m

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

        physics = np.zeros((states.shape[0], 12))

        for i, (s, t) in enumerate(zip(states, time)):

            w = s[0::2]
            dw = s[1::2]

            eval, S, J, H = self.surface.SJH(*w)

            F = self.forces.eval(w, dw, t, S, J)

            V = J @ dw.T
            normV = np.linalg.norm(V, 2)

            physics[i] = np.concatenate([
                S,
                V,
                F,
                [normV],
                [np.linalg.norm(F, 2)],
                [0.5 * self.m * normV**2]
            ])

        return physics


class SurfaceGuidedFallMassSystem(SurfaceGuidedMassSystem):
    def __init__(self, surface: Surface, s0: np.ndarray = None, m: float = 1.0, g: np.ndarray = None):
        super(SurfaceGuidedFallMassSystem, self).__init__(
            surface, s0, m, Gravity(m, g)
        )
