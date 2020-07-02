import abc

from typing import Iterable, Union, Tuple

from ..indexes import *

import numpy as np

# eval return 18 elements long
# 18 elements list
# =====
# x y z
# =====
# ∂_u X  ∂_v X
# ∂_u Y  ∂_v Y
# ∂_u Z  ∂_v Z
# =====
# ∂_u^2 X       ∂_(u,v)^2 X
# ∂_(u,v)^2 X   ∂_v^2 X
# =====
# ∂_u^2 Y       ∂_(u,v)^2 Y
# ∂_(u,v)^2 Y   ∂_v^2 Y
# =====
# ∂_u^2 Z       ∂_(u,v)^2 Z
# ∂_(u,v)^2 Z   ∂_v^2 Z

class Surface(abc.ABC):
    plimits = [
        (0.0, 1.0),  # u
        (0.0, 1.0),  # v
    ]

    @staticmethod
    def position(eval: np.ndarray):
        return np.array(eval[:zi + 1])

    @staticmethod
    def jacobian(eval: np.ndarray):
        return np.array(eval[duxi: duxi + 6]).reshape((3, 2))

    # x : xyz = 0
    # y : xyz = 1
    # z : xyz = 2
    @staticmethod
    def hessian(eval: np.ndarray, xyz=0):
        shift = xyz*3
        return np.array([
            [eval[duuxi + shift], eval[duvxi + shift]],
            [eval[duvxi + shift], eval[dvvxi + shift]]
        ])

    @staticmethod
    def dim_hessian(eval: np.ndarray):
        return np.array([
            Surface.hessian(eval, xyz=X) for X in xyz
        ])

    # return all Du Dv Duu Dvv Duv of x y z
    @abc.abstractmethod
    def eval(self, u: float, v: float) -> np.ndarray:
        raise NotImplementedError()

    def SJH(self, u: float, v: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        eval = self.eval(u, v)

        return (
            eval,
            self.position(eval),
            self.jacobian(eval),
            self.dim_hessian(eval)
        )

    # return rebuild evals for data
    def trajectory(self, uv: np.ndarray) -> np.ndarray:
        evals = np.zeros((uv.shape[0], 3))

        for i, (u, v) in enumerate(uv):
            evals[i] = self.position(self.eval(u, v))

        return evals


    def mesh(self, umesh=50, vmesh=50):
        return (
            np.linspace(*self.plimits[ui], umesh),
            np.linspace(*self.plimits[vi], vmesh),
        )

    # U, V must be 1d arrays
    def buildsurface(self, U: np.ndarray, V: np.ndarray):
        mesh = np.zeros((3, U.shape[0], V.shape[0]))

        for i, u in enumerate(U):
            for j, v in enumerate(V):
                mesh[:, i, j] = self.position(self.eval(u, v))

        return mesh