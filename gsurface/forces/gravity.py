from .force import ConservativeForce, np


class Gravity(ConservativeForce):
    def __init__(self, m: float = 1.0, g: np.ndarray = None):
        self.m: float = m

        if g is None:
            g = np.array([0.0, 0.0, -9.81])

        self.g: np.ndarray = g

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return self.m*self.g

    def potential(self, t: float, S: np.ndarray) -> float:
        return -self.m*np.vdot(self.g, S)

    def __repr__(self):
        return super(Gravity, self).__repr__() + " {g} m/s²".format(**self.__dict__)
