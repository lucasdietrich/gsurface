# todo experimental

import numpy as np

from .force import ConservativeForce


# https://fr.wikipedia.org/wiki/%C3%89lectromagn%C3%A9tisme
class StaticFieldElectroMagneticForce(ConservativeForce):
    def __init__(self, q: float, E: np.ndarray, B: np.ndarray = None, **kargs):
        """
        Electromagnetic force in static E and B fields : F = q (E + V x B)
        :param q: charge (C)
        :param E: electric field (V/m)
        :param B: magnetic field (T)
        """
        if B is None:
            B = np.zeros((3,))

        self.q = float(q)
        self.B = np.array(B)
        self.E = np.array(E)

    def potential(self, t: float, S: np.ndarray) -> float:
        return - self.q * np.vdot(self.E, S)

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        return self.q * (self.E + np.vdot(V, self.B))


class MagnetForce(ConservativeForce):
    def __init__(self):
        raise NotImplementedError()

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        raise NotImplementedError()

    def potential(self, t: float, S: np.ndarray) -> float:
        raise NotImplementedError()