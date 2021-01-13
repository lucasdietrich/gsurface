from typing import Tuple

from .force import ConservativeForce, np


# long range gravity
class Gravity(ConservativeForce):
    def __init__(self, m: float = 1.0, g: np.ndarray = None, **kargs):
        self.m: float = m

        if g is None:
            g = np.array([0.0, 0.0, -9.81])

        self.g: np.ndarray = np.array(g)

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return self.m*self.g

    def potential(self, t: float, S: np.ndarray) -> float:
        return -self.m*np.vdot(self.g, S)

    __repr_str__ = "g = {g} m s^-2"


# short term gravity
# G = by default 1.0
class NewtonGravity(ConservativeForce):
    def __init__(self, m: float = 1.0, M: float = 1.0, G: float = 1.0, clip: np.ndarray = None, **kargs):
        self.m = m
        self.M = m
        self.G = G

        self.product = self.G * self.M * self.m

        if clip is None:
            self.clip = np.zeros((3,))

        self.clip = np.array(clip)

    def radius(self, S: np.ndarray) -> Tuple[np.ndarray, float]:
        r = S - self.clip
        rn = np.linalg.norm(r)

        return r, rn

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        r, rn = self.radius(S)

        return - self.product * r / rn**3

    def potential(self, t: float, S: np.ndarray) -> float:
        r, rn = self.radius(S)

        return - self.product / rn

    __repr_str__ = "m = {m:.2f} kg, M = {M:.2f} kg, G = {M:.2f} m^3 kg^-1 s^-2 "
