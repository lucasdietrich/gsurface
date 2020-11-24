import abc

from .force import Force, np


class ViscousFriction(Force):
    def __init__(self, mu: float = 1.0, **kargs):
        self.mu = mu

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return -self.mu * J @ dw.T

    __repr_str__ = "mu = {mu:.2f} N.s/m"


# https://fr.wikipedia.org/wiki/Chute_avec_r%C3%A9sistance_de_l%27air
# R = 1/2 Cx p S v^2
class AirFriction(Force):
    # Cx : [1]
    # S : m^2
    # rho kg/m3
    def __init__(self, Cx: float = 1.0, S: float = 0.0025, rho: float = 1.225, **kargs):
        self.Cx = Cx
        self.S = S
        self.rho = rho

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        v = J @ dw.T

        return - 0.5 * self.Cx * self.S * self.rho * v * np.linalg.norm(v, 2)

    __repr_str__ = "Cx = {Cx:.2f}, S = {S:.2f} m^2, rho = {rho:.2f} kg m^-3"


class DirectedViscousFriction(ViscousFriction, abc.ABC):
    @abc.abstractmethod
    def direction(self, t: float, S: np.ndarray) -> np.ndarray:
        raise NotImplemented

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        # eval direction
        direction = self.direction(t, S)

        # eval 3D speed
        V = J @ dw.T

        # eval coeff
        alpha = np.dot(V, direction)

        # apply coff
        return - self.mu * alpha * np.linalg.norm(V) * direction


class ConstantDirectedViscousFriction(DirectedViscousFriction):
    def __init__(self, mu: float = 1.0, direction: np.ndarray = None):
        if direction is None:
            direction = np.array([1.0, 0.0, 0.0])

        self.direction_vector = np.array(direction)
        
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
        delta = S - self.clip
        return delta / np.linalg.norm(delta)

    __repr_str__ = DirectedViscousFriction.__repr_str__ + ", clip = {clip}"
