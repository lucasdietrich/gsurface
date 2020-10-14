from .force import Force, np


class ViscousFriction(Force):
    def __init__(self, mu: float = 1.0):
        self.mu = mu

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return -self.mu * J @ dw.T

    def __repr__(self):
        return super(ViscousFriction, self).__repr__() + " mu = {mu}".format(**self.__dict__)


# https://fr.wikipedia.org/wiki/Chute_avec_r%C3%A9sistance_de_l%27air
# R = 1/2 Cx p S v^2
class AirFriction(Force):
    # Cx : [1]
    # S : m^2
    # rho kg/m3
    def __init__(self, Cx: float = 1.0, S: float = 0.0025, rho: float = 1.225):
        self.Cx = Cx
        self.S = S
        self.rho = rho

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        v = J @ dw.T

        return - 0.5 * self.Cx * self.S * self.rho * v * np.linalg.norm(v, 2)

    def __repr__(self):
        return super(AirFriction, self).__repr__() + \
               " Cx = {Cx}, S = {S} m², rho = {rho} kg/m^3".format(**self.__dict__)
