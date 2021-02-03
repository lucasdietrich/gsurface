import abc

from gsurface import utils
from .force import Force, np


class ViscousFriction(Force):
    def __init__(self, mu: float = 1.0, **kargs):
        self.mu = mu

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        return -self.mu * V

    __repr_str__ = "mu = {mu:.2f} N.s/m"


# https://fr.wikipedia.org/wiki/Chute_avec_r%C3%A9sistance_de_l%27air
# R = 1/2 Cx p S v^2
class AirFriction(Force):
    # Cx : [1]
    # S : m^2
    # rho kg/m3
    def __init__(self, Cx: float = 1.0, S: float = 0.0025, rho: float = 1.225, **kargs):
        self.Cx = float(Cx)
        self.S = float(S)
        self.rho = float(rho)

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        return - 0.5 * self.Cx * self.S * self.rho * V * np.linalg.norm(V, 2)

    __repr_str__ = "Cx = {Cx:.2f}, S = {S:.2f} m^2, rho = {rho:.2f} kg m^-3"


class DirectedViscousFriction(ViscousFriction, abc.ABC):
    @abc.abstractmethod
    def direction(self, t: float, S: np.ndarray) -> np.ndarray:
        raise NotImplemented

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        # eval direction
        direction = self.direction(t, S)

        # eval coeff
        alpha = np.dot(V, direction)

        # apply coff
        return - self.mu * alpha * np.linalg.norm(V) * direction


class ConstantDirectedViscousFriction(DirectedViscousFriction):
    def __init__(self, mu: float = 1.0, direction_vector: np.ndarray = None):
        if direction_vector is None:
            direction_vector = np.array([1.0, 0.0, 0.0])

        self.direction_vector = np.array(direction_vector)
        
        super().__init__(mu)

    def direction(self, t: float, S: np.ndarray) -> np.ndarray:
        return self.direction_vector

    __repr_str__ = DirectedViscousFriction.__repr_str__ + ", direction : {direction_vector}"


class CenterDirectedViscousFriction(DirectedViscousFriction):
    def __init__(self, mu: float = 1.0, clip: np.ndarray = None):
        if clip is None:
            clip = np.zeros((3,))

        self.clip = np.array(clip)

        super().__init__(mu)

    def direction(self, t: float, S: np.ndarray) -> np.ndarray:
        delta, dist = utils.distance(S - self.clip)
        return delta / dist

    __repr_str__ = DirectedViscousFriction.__repr_str__ + ", clip = {clip}"


class SolidForce(Force):
    def __init__(self, intensity: np.ndarray):
        self.intensity = np.array(intensity)

    def eval(self, t: float, S: np.ndarray = None, V: np.ndarray = None) -> np.ndarray:
        return self.intensity * utils.direction(V)
