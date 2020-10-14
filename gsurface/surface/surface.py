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

    # line 1 : u lims /  line 2 : v lims
    plimits = np.ones((2, 2))

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

    def translate(self, shiftvector: np.ndarray):
        self.shiftvector: np.ndarray = shiftvector

    def rotate(self, rotmat: np.ndarray):
        self.rotmat: np.ndarray = rotmat

    @staticmethod
    def jacobian(e: np.ndarray):
        return np.array(e[duxi: duxi + 6]).reshape((3, 2))

    # x : xyz = 0
    # y : xyz = 1
    # z : xyz = 2
    @staticmethod
    def hessian(e: np.ndarray, X=0):
        shift = X * 3
        return np.array([
            [e[duuxi + shift], e[duvxi + shift]],
            [e[duvxi + shift], e[dvvxi + shift]]
        ])

    @staticmethod
    def dim_hessian(e: np.ndarray):
        return np.array([
            Surface.hessian(e, X=X) for X in xyz
        ])

    def process_transformations(
            self,
            x=0, y=0, z=0,
            dux=0, dvx=0, duy=0,
            dvy=0, duz=0, dvz=0,
            duux=0, duvx=0, dvvx=0,
            duuy=0, duvy=0, dvvy=0,
            duuz=0, duvz=0, dvvz=0
    ):
        e = np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])

        # apply translation
        e[: zi + 1] += self.shiftvector

        # apply rotation
        # todo notimplemented

        return e


    # return all Du Dv Duu Dvv Duv of x y z
    @abc.abstractmethod
    def eval(self, u: float, v: float) -> np.ndarray:
        raise NotImplementedError()

    def SJH(self, u: float, v: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        e = self.eval(u, v)

        return (
            e,
            e[ixe_position],
            self.jacobian(e),
            self.dim_hessian(e)
        )

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
                mesh[:, i, j] = self.eval(u, v)[ixe_position]

        return mesh

    # todo translation only affect S
    # def translate(self, x: np.ndarray) -> Surface:
    #     raise NotImplementedError()

    # todo rotation only affect S
    # def rotate(self, x: np.ndarray, angle: float) -> Surface:
    #     raise NotImplementedError()

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
    __repr_ljust__ = 50

    def __repr__(self):
        return (
            "Surface:{0}" + self.__repr_str__
        ).format(self.__class__.__name__, **self.__dict__).ljust(self.__repr_ljust__)