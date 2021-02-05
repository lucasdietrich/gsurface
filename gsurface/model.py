from typing import Union, Iterable

import numpy as np
from gsurface.advanced.ode.system import ODESystem

from gsurface.serialize import SerializableInterface
from .forces import Force, ForceSum
from .indexes import *
from .solid import SOLID, toSolid
from .surface.surface import Surface


def build_s0(u0: float = 0.0, du0: float = 0.0, v0: float = 0.0, dv0: float = 0.0):
    return np.array([u0, du0, v0, dv0])


ForcesType = Union[Force, ForceSum, Iterable[Force]]


class SurfaceGuidedMassSystem(ODESystem, SerializableInterface):
    def __init__(
            self, surface: Surface,
            s0: np.ndarray = None,
            solid: SOLID = 1.0,
            forces: ForcesType = None,
            **kargs
    ):
        """
        Create a model of a single mass bound to a surface, with initial position s0 and subjected to forces.

        Args:
            surface: Surface
            s0: initial state [u0, du0, v0, dv0]
            solid: Solid mass
            forces: Resulting force
            **kargs:
        """
        self.surface: Surface = surface

        self.forces: ForceSum = ForceSum(forces)

        if s0 is None:
            s0 = build_s0()

        self.solid = toSolid(solid)

        super(SurfaceGuidedMassSystem, self).__init__(s0)

    def __repr__(self):
        return f"{self.__class__.__name__} for solid {self.solid} on surface {self.surface} " \
               f"with s0 = {self.s0}\n" \
               f"and forces : {self.forces}"

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        """
        Deriv function

        :param s:
        :param t:
        :return:
        """
        # vars
        w = s[::2]
        dw = s[1::2]

        # todo simplify/optimize eval
        S, J, H = self.surface.eval(*w)

        V = J @ dw.T

        # feed all interacted forces

        # eval force:
        F = self.forces.eval(t, S, V)

        # eval and return
        return self.ds(dw, F, J, H)

    def ds(self, dw: np.ndarray, F: np.ndarray, J: np.ndarray, H: np.ndarray) -> np.ndarray:
        """
        Evaluate resulating elementary system variation for the elementary variation of parameters dw on the surface

        Args:
            dw: elementary variation of parameters
            F: resulting force
            J: surface jacobian
            H: surface hessians

        Returns: resulting elementary system variation
        """
        # vars
        du, dv = dw

        # build intermediate symbols
        Duu, Dvv = np.sum(J**2, axis=0)

        Puv = np.vdot(J[:, ui], J[:, vi])

        wHw = dw.T @ H @ dw

        G = wHw - F / self.solid.mass

        Ru, Rv = np.dot(G, J)

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

    def solutions(self, states: np.ndarray, time: np.ndarray):
        """
        Evaluate main physical quantities from model solution
            Surface position, Speed, Resulting force, Speed norm, Force norm, Kinetic energy, Potential energy,
            System mecanical energy

        Args:
            states: @return from solve method
            time: time mesh

        Returns:
        """
        assert states.shape[0] == time.shape[0]

        physics = np.zeros((states.shape[0], 14))

        for i, (s, t) in enumerate(zip(states, time)):

            w = s[0::2]
            dw = s[1::2]

            S, J, H = self.surface.eval(*w)

            V = J @ dw.T

            F = self.forces.eval(t, S, V)

            normV = np.linalg.norm(V, 2)

            Ek = 0.5 * self.solid.mass * normV**2
            Ep = np.sum(force.potential(t, S) for force in self.forces.get_conservative_forces())
            Em = Ek + Ep

            physics[i] = np.concatenate([
                S,
                V,
                F,
                [
                    normV,
                    np.linalg.norm(F, 2),
                    Ek,
                    Ep,
                    Em,
                ]
            ])

        return physics

    def todict(self) -> dict:
        d = super(SurfaceGuidedMassSystem, self).todict().copy()

        d.update({
            "forces": self.forces.forces
        })

        return d
