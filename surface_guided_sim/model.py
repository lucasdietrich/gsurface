from ode.system import ODESystem

import numpy as np

import abc

ui, vi = 0, 0

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

class SurfaceGuidedFallSystem(ODESystem):
    def __init__(self, sys: Surface):
        self.sys = sys

        s0 = np.array([
            0.0,    # u
            1.0,    # vu
            0.0,    # v
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
        ds = np.copy(s)

        u, v = s[0], s[2]

        w = np.array([u, v]).transpose()

        du, dv = s[1], s[3]

        # eval
        eval = self.sys.eval_all(u, v)

        # eval force:
        F = self.force(u, v, t, eval)

        # builds matrices
        J = self.jacobian(eval)
        H = self.dim_hessian(eval)

        # build intermediate symbols
        Duu = np.sum(J[X, ui]**2 for X in xyz)
        Dvv = np.sum(J[X, vi]**2 for X in xyz)

        wT_HSX_w = lambda X: w.transpose() @ H[X] @ w

        # build common mult
        Puv = np.sum(
            J[X, ui] * J[X, vi] for X in xyz
        )

        # build residual
        Ru = np.sum(
            J[X, ui] * wT_HSX_w(X) for X in xyz
        ) - np.vdot(F, J[:, ui]) / self.m

        Rv = np.sum(
            J[X, vi] * wT_HSX_w(X) for X in xyz
        ) - np.vdot(F, J[:, vi]) / self.m

        D = Duu * Dvv - Puv**2

        # build der state
        # u
        ds[0] = du
        ds[1] = (Rv*Puv - Ru*Dvv) / D

        # v
        ds[2] = dv
        ds[3] = (Ru*Puv - Rv*Duu) / D

        return ds



