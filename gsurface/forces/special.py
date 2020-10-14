import numpy as np

from .force import Force

from ..model import SurfaceGuidedMassSystem


class SpecialForce(Force):
    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return np.zeros((3,))
