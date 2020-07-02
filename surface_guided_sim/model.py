from ode.system import ODESystem

from .surface.surface import Surface

import numpy as np

from .indexes import *

from typing import Callable

ForceType = Callable[
                [float, float, float, np.ndarray, np.ndarray, np.ndarray],
                np.ndarray
            ]


class SurfaceGuidedMassSystem(ODESystem):
    def __init__(
            self, surface: Surface,
            s0: np.ndarray = None,
            m: float = 1.0,
            force: ForceType = None
    ):
        self.surface: Surface = surface

        self.force: ForceType = force

        if s0 is None:
            s0 = np.array([
                0.0,  # u
                0.0,  # vu
                0.0,  # v
                0.0  # vu
            ])

        self.m = m

        super(SurfaceGuidedMassSystem, self).__init__(s0)

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        u, du, v, dv = s

        dw = np.array([du, dv])

        # eval
        eval, S, J, H = self.surface.SJH(u, v)

        # eval force:
        F = self.force(u, v, t, S, J, H)

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
    def __init__(self, surface: Surface, s0: np.ndarray = None, m: float = 1.0, g: float = 9.81, dir: np.ndarray = None):
        self.g = g

        if dir is None:
            dir = np.array([
                0.0,
                0.0,
                -1.0
            ])

        self.dir = dir

        super(SurfaceGuidedFallMassSystem, self).__init__(
            surface, s0, m, self.force
        )

    def force(self, u: float, v: float, t: float, S: np.ndarray, J: np.ndarray, H: np.ndarray):
        return self.m * self.g * self.dir / np.linalg.norm(self.dir, 2)


