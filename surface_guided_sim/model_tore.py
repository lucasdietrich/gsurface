from ode.system import ODESystem

import numpy as np

[
    xi, yi, zi,
    duxi, dvxi, duyi, dvyi, duzi, dvzi,
    duuxi, duvxi, dvvxi, duuyi, duvyi, dvvyi, duuzi, duvzi, dvvzi
] = list(range(18))

class SurfaceTore:
    def __init__(self, r=0.5, R=1.0):
        self.r = r
        self.R = 1.0

        # check constraints

        # generate domain for u and v

    # return in the following order:
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
    def eval(self, u, v, pos_only = False):
        Rrcos = self.R + self.r*np.cos(v)

        x = Rrcos*np.cos(u)
        y = Rrcos*np.sin(u)
        z = self.r*np.sin(v)

        # position only
        if pos_only:
            return [
                x, y, z
            ]

        dux = -y
        dvx = -self.r*np.sin(v)*np.cos(u)

        duy = x
        dvy = -self.r*np.sin(v)*np.sin(u)

        duz = 0
        dvz = self.r*np.cos(v)

        duux = -x
        duvx = -dvy
        dvvx = -dvz*np.cos(u)

        duuy = -y
        duvy = -dvx
        dvvy = -dvz*np.sin(u)

        duuz = 0
        duvz = 0
        dvvz = -z

        return [
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ]

class SurfaceGuidedFallSystem(ODESystem):
    def __init__(self, sys: SurfaceTore):
        self.sys = sys

        s0 = np.array([
            0.0,    # u
            1.0,    # vu
            0.0,    # v
            0.0     # vu
        ])

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

    def _derivs(self, s: np.ndarray, x: float) -> np.ndarray:
        ds = np.copy(s)

        u, v = s[0], s[2]

        ds[0] = s[1] # du
        ds[2] = s[3] # dv

        # eval
        eval = self.sys.eval(u, v)

        # builds matrices
        jacobian = self.jacobian(eval)
        hessians = [
            self.hessian(eval, 0),
            self.hessian(eval, 1),
            self.hessian(eval, 2),
        ]

        # u
        ds[1] = 0

        ds[2] = 0

        return ds



