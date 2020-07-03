from .force import Force, np


class Gravity(Force):
    def __init__(self, m: float = 1.0, g: np.ndarray = None):
        self.m: float = m

        if g is None:
            g = np.array([0.0, 0.0, -9.81])
        self.g: np.ndarray = g

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        return self.m*self.g

    def __repr__(self):
        return super(Gravity, self).__repr__() + " {g} m/s²".format(**self.__dict__)