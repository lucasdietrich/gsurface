from ode.system import ODESystem

from .surface.surface import Surface

import numpy as np

from .indexes import *

from typing import Callable, Union, Iterable

from .forces import Force, Gravity, NoForce, ForceSum


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

        wHw = dw.T @ H @ dw

        # build common mult
        Puv = np.sum(J[:, ui] * J[:, vi])

        # build residual
        Ru = np.sum(J[:, ui] * wHw) - np.vdot(F, J[:, ui]) / self.m
        Rv = np.sum(J[:, vi] * wHw) - np.vdot(F, J[:, vi]) / self.m

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


class SurfaceGuidedFallMassSystem(SurfaceGuidedMassSystem):
    def __init__(self, surface: Surface, s0: np.ndarray = None, m: float = 1.0, g: np.ndarray = None):
        super(SurfaceGuidedFallMassSystem, self).__init__(
            surface, s0, m, Gravity(m, g)
        )


