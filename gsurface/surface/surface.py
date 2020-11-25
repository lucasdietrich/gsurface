from __future__ import annotations

import abc

import numpy as np
from scipy.integrate import dblquad

from gsurface.serialize.interface import SerializableInterface
from .transformations import GetTransformationStrategy
from .transformations import TransformationStrategy
from ..indexes import *
from ..types import SJH


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


# todo update strategy when modifying shitvector or rotmat attributes directly


class Surface(abc.ABC, SerializableInterface):
    def __init__(self, plimits: np.ndarray = None, shiftvector: np.ndarray = None, rotmat: np.ndarray = None):
        if plimits is None:
            plimits = np.array([
                [-1.0, 1.0],
                [-1.0, 1.0]
            ])
        elif plimits.shape != (2, 2):
            raise Exception("Parameters limits must be of size 2x2")

        if shiftvector is None:
            shiftvector = np.zeros((3,))

        # choose strategy
        elif shiftvector.shape != (3,):
            raise Exception("Shift vector must be of shape 3")

        if rotmat is None:
            rotmat = np.identity(3)

            # choosy strategy
        elif rotmat.shape != (3, 3):
            raise Exception("Rotational matrice must be of shape 3x3")

        self.plimits = np.array(plimits)

        # choose strategy
        self.transformation: TransformationStrategy = GetTransformationStrategy(shiftvector, rotmat)

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

    # shiftvector setter
    def translate(self, shiftvector: np.ndarray) -> Surface:
        self.transformation = GetTransformationStrategy(shiftvector, self.transformation.M)

        return self

    # todo add rotation
    #  numpy rotation matrices help : https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
    # rotmat setter
    def rotate(self, rotmat: np.ndarray) -> Surface:
        self.transformation = GetTransformationStrategy(self.transformation.D, rotmat)

        return self

    # set translate and rotation matrix from serialized data
    # + plimits
    @classmethod
    def fromdict(cls, d: dict):
        surface: Surface = super().fromdict(d)

        ## todo apply transformation

        surface.transformation = d["transformation"]

        if "plimits" in d:
            surface.plimits = np.array(d["plimits"])

        return surface

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

    # add strategy for shift/rot

    # newS = D + M*S
    def _process_transformations(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return self.transformation.apply(S, J, H)

    # return all Du Dv Duu Dvv Duv of x y z
    @abc.abstractmethod
    def _definition(self, u: float, v: float) -> SJH:
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

    def _dS(self, u: float, v: float) -> float:
        """
        Infinitesimal area function on position (u, v)

        :param u:
        :param v:
        :return: dS = sqrt(|fu|²|fv|² - |fu . fv|²)
        """
        S, J, H = self.eval(u, v)

        fu, fv = J.T

        E = np.linalg.norm(fu)**2
        F = np.linalg.norm(fv)**2
        G = np.dot(fu, fv)**2

        return np.sqrt(E*F - G**2)

    def area(self, epsabs=1.49e-8, epsrel=1.49e-8) -> float:
        """
        Calculate area of the surface for u, v in U, V = plimits
        :param epsabs: @see scipy.integrate.dblquad
        :param epsrel: @see scipy.integrate.dblquad
        :return:
        """
        return dblquad(
            self._dS,
            a=self.plimits[0,0],
            b=self.plimits[0,1],
            gfun=lambda u: self.plimits[1, 0],
            hfun=lambda u: self.plimits[1, 1],
            epsabs=epsabs,
            epsrel=epsrel
        )[0]

    __repr_str__ = ""
    __repr_ljust__ = 30

    def __repr__(self):
        return (
            "Surface:{0}" + self.__repr_str__ + " {transformation}"
        ).format(self.__class__.__name__, **self.__dict__).ljust(self.__repr_ljust__)
