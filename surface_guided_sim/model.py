from ode.system import ODESystem

import numpy as np

import abc

from typing import Iterable, Union

ui, vi = 0, 1

xyz = range(3)

[
    xi, yi, zi,
    duxi, dvxi, duyi, dvyi, duzi, dvzi,
    duuxi, duvxi, dvvxi, duuyi, duvyi, dvvyi, duuzi, duvzi, dvvzi
] = list(range(18))

# eval return 18 elements long
# 18 elements list
# =====
# x
# y
# z
# ∂_u X
# ∂_v X
# ∂_u Y
# ∂_v Y
# ∂_u Z
# ∂_v Z
# ∂_u^2 X
# ∂_(u,v)^2 X
# ∂_v^2 X
# ∂_u^2 Y
# ∂_(u,v)^2 Y
# ∂_v^2 Y
# ∂_u^2 Z
# ∂_(u,v)^2 Z
# ∂_v^2 Z
class Surface(abc.ABC):
    # return position x, y, z in a 1D vector
    def eval(self, u: float, v: float) -> np.ndarray:
        raise NotImplementedError()

    # return all Du Dv Duu Dvv Duv of x y z
    def eval_all(self, u: float, v: float) -> np.ndarray:
        raise NotImplementedError()

    # return rebuild evals for data
    def evals(self, uv: np.ndarray) -> np.ndarray:
        evals = np.zeros((uv.shape[0], 3))

        for i, (u, v) in enumerate(uv):
            evals[i] = self.eval(u, v)

        return evals

    # U, V must be 1d arrays
    def mesh(self, U: np.ndarray, V: np.ndarray):
        mesh = np.zeros((3, U.shape[0], V.shape[0]))

        for i, u in enumerate(U):
            for j, v in enumerate(V):
                mesh[:, i, j] = self.eval(u, v)

        return mesh


class SurfaceGuidedFallSystem(ODESystem):
    def __init__(self, surface: Surface):
        self.surface = surface

        s0 = np.array([
            0.0,    # u
            0.0,    # vu
            1.0,    # v
            0.0     # vu
        ])

        self.m = 1.0

        super(SurfaceGuidedFallSystem, self).__init__(s0)

    def jacobian(self, eval):
        return np.array(eval[duxi: duxi + 6]).reshape((3, 2))

    # x : xyz = 0
    # y : xyz = 1
    # z : xyz = 2
    def hessian(self, eval, xyz=0):
        shift = xyz*3
        return np.array([
            [eval[duuxi + shift], eval[duvxi + shift]],
            [eval[duvxi + shift], eval[dvvxi + shift]]
        ])

    def dim_hessian(self, eval):
        return np.array([
            self.hessian(eval, xyz=X) for X in xyz
        ])

    def force(self, u, v, t, eval):
        return np.array([
            0.0,
            0.0,
            0.0
        ])

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        u, du, v, dv = s

        dw = np.array([du, dv])

        # eval
        eval = self.surface.eval_all(u, v)

        # eval force:
        F = self.force(u, v, t, eval)

        # builds matrices
        J = self.jacobian(eval)
        H = self.dim_hessian(eval)

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



