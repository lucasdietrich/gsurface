from __future__ import annotations

import abc
from typing import Tuple

import numpy as np

from ..indexes import *


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
    plimits = np.array([
        [-1.0, 1.0],  # u lims
        [-1.0, 1.0]   # v lims
    ])

    def multlims(self, k: float = 2.0) -> Surface:
        self.plimits *= k
        return self

    def setlims(self, u_ll: float = None, u_ul: float = None, v_ll: float = None, v_ul: float = None) -> Surface:
        if u_ll is not None:
            self.plimits[ui, 0] = u_ll

        if u_ul is not None:
            self.plimits[ui, 1] = u_ul

        if v_ll is not None:
            self.plimits[vi, 0] = v_ll

        if v_ul is not None:
            self.plimits[vi, 1] = v_ul

        return self

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

    @staticmethod
    def buildevalreturn(
            x=0, y=0, z=0,
            dux=0, dvx=0, duy=0,
            dvy=0, duz=0, dvz=0,
            duux=0, duvx=0, dvvx=0,
            duuy=0, duvy=0, dvvy=0,
            duuz=0, duvz=0, dvvz=0
    ):
        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
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

    # vectorial speed
    def speed(self, data: np.ndarray) -> np.ndarray:
        speed = np.zeros((data.shape[0], 3))

        for i, (u, du, v, dv) in enumerate(data):
            eval, S, J, H = self.SJH(u, v)

            dw = np.array([du, dv])

            speed[i] = J @ dw.T

        return speed

    # todo, optimisation, calculer traj et speed en même temps
    # todo faire le calcul direct dans le sim principale
    # def traj_speed(self, data: np.ndarray) -> np.ndarray:


    def mesh(self, nu=50, nv=50):
        return (
            np.linspace(*self.plimits[ui], nu),
            np.linspace(*self.plimits[vi], nv),
        )

    # U, V must be 1d arrays
    def buildsurface(self, U: np.ndarray, V: np.ndarray):
        mesh = np.zeros((3, U.shape[0], V.shape[0]))

        for i, u in enumerate(U):
            for j, v in enumerate(V):
                mesh[:, i, j] = self.position(self.eval(u, v))

        return mesh