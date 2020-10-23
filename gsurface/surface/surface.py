from __future__ import annotations

import abc
from typing import Tuple

import numpy as np

from ..indexes import *

SJH = Tuple[np.ndarray, np.ndarray, np.ndarray]

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

    # line 1 : u lims /  line 2 : v lims
    plimits = np.array([
        [-1.0, 1.0],
        [-1.0, 1.0]
    ])

    shiftvector = np.zeros((3,))

    rotmat = np.identity(3)

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

    def translate(self, shiftvector: np.ndarray) -> Surface:
        self.shiftvector: np.ndarray = shiftvector

        return self

    def rotate(self, rotmat: np.ndarray) -> Surface:
        raise NotImplementedError

        self.rotmat: np.ndarray = rotmat

        return self

    # x : xyz = 0
    # y : xyz = 1
    # z : xyz = 2
    @staticmethod
    def _hessian(e: np.ndarray, X=0):
        shift = X * 3
        return np.array([
            [e[duuxi + shift], e[duvxi + shift]],
            [e[duvxi + shift], e[dvvxi + shift]]
        ])

    @staticmethod
    def buildMetric(
            x=0.0, y=0.0, z=0.0,
            dux=0.0, dvx=0.0, duy=0.0,
            dvy=0.0, duz=0.0, dvz=0.0,
            duux=0.0, duvx=0.0, dvvx=0.0,
            duuy=0.0, duvy=0.0, dvvy=0.0,
            duuz=0.0, duvz=0.0, dvvz=0.0
    ) -> SJH:

        S = np.array([x, y, z])

        # jacobian
        J = np.array([
            [dux, dvx],
            [duy, dvy],
            [duz, dvz]
        ])

        # dim hessian
        H = np.array([
            [
                [duux, duvx],
                [duvx, dvvx],
            ],
            [
                [duuy, duvy],
                [duvy, dvvy],
            ],
            [
                [duuz, duvz],
                [duvz, dvvz],
            ],
        ])

        return S, J, H

    def _process_transformations(self, S: np.ndarray, J: np.ndarray, H: np.ndarray):
        # apply translation
        S += + self.shiftvector

        # apply rotation
        # todo notimplemented

        return S, J, H

    # return all Du Dv Duu Dvv Duv of x y z
    @abc.abstractmethod
    def _definition(self, u: float, v: float) -> dict:
        raise NotImplementedError

    def eval(self, u: float, v: float) -> SJH:
        return self._process_transformations(*self._definition(u, v))

    # todo, optimisation, calculer traj et speed en même temps
    # todo faire le calcul direct dans le sim principale
    # def traj_speed(self, data: np.ndarray) -> np.ndarray:

    def mesh(self, nu=50, nv=50):
        return (
            np.linspace(*self.plimits[ui], nu),
            np.linspace(*self.plimits[vi], nv),
        )

    # U, V must be 1d arrays
    def build_surface(self, U: np.ndarray, V: np.ndarray):
        mesh = np.zeros((3, U.shape[0], V.shape[0]))

        for i, u in enumerate(U):
            for j, v in enumerate(V):
                mesh[:, i, j] = self.eval(u, v)[Si]

        return mesh

    # check integrity
    def check(self, nu: int = 20, nv: int = 20, tolerance=1e-7):
        from . import diff

        emat = diff.get_diff_surface_errors(self, *self.mesh(nu, nv))

        return np.max(emat) <= tolerance

    # check integrity
    def check_verbose(self, nu: int = 20, nv: int = 20, tolerance=1e-7):
        from . import diff

        emat = diff.get_diff_surface_errors(self, *self.mesh(nu, nv))

        elist = np.max(emat, axis=(1, 2))

        index_str = ["xi", "yi", "zi", "duxi", "dvxi", "duyi", "dvyi", "duzi", "dvzi"]

        print("=== Checking surface definition ===")
        print("U {0} points from {1} to {2}".format(nu, *self.plimits[0]))
        print("V {0} points from {1} to {2}".format(nv, *self.plimits[1]))
        print("Tolerance : {0:.1E}".format(tolerance))

        for index in range(duuxi):
            print("index[{0} : {1}] max err = {2:.1E} [{3}]".format(
                index, index_str[index], elist[index], elist[index] <= tolerance
            ))

        return np.max(elist) <= tolerance

    __repr_str__ = ""
    __repr_ljust__ = 30

    def __repr__(self):
        return (
            "Surface:{0}" + self.__repr_str__
        ).format(self.__class__.__name__, **self.__dict__).ljust(self.__repr_ljust__)
