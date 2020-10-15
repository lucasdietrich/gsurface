from .force import ConservativeForce, np


# l0 = 0, linear spring force
# F = -K (CS - l0) dir(CS_v)
# as l0 = 0
# F = -k CS dir(CS_v)
# F = -k CS_v
# F = -k (S - C)
class SpringForce(ConservativeForce):
    def __init__(self, stiffness: float = 1.0, clip: np.ndarray = None):
        self.stiffness = stiffness

        if clip is None:
            clip = np.array([0.0, 0.0, 0.0])

        self.clip = clip

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return -self.stiffness*(S - self.clip)

    def potential(self, t: float, S: np.ndarray) -> float:
        return 0.5*self.stiffness * np.linalg.norm(S - self.clip, 2)**2

    def __repr__(self):
        return super(SpringForce, self).__repr__() + \
               " stiffness = {stiffness} N/m, clip = {clip}".format(**self.__dict__)


# F = -K (CS - l0) dir(CS_v)
# F = -K (CS - l0) (CS_v / CS)
# F = -K (1 - l0/CS) CS_v
class LengthedSpringForce(SpringForce):
    def __init__(self, stiffness: float = 1.0, clip: np.ndarray = None, l0: float = 1.0):
        if l0 == 0.0:
            print("Use of LengthedSpringForce for l0 = 0.0 is depreciated, use SpringForce instead")

        self.l0 = l0

        super(LengthedSpringForce, self).__init__(stiffness, clip)

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        CS_vec = S - self.clip
        CS = np.linalg.norm(CS_vec)

        if CS == 0:
            return np.zeros((3,))
        else:
            return -self.stiffness*(1 - self.l0 / CS) * CS_vec

    def potential(self, t: float, S: np.ndarray) -> float:
        return 0.5*self.stiffness*(np.linalg.norm(S - self.clip) - self.l0)**2

    def __repr__(self):
        return super(LengthedSpringForce, self).__repr__() + ", l0 = {l0} m".format(**self.__dict__)
