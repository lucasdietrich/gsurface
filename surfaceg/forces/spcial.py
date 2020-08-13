import numpy as np

from .force import Force

from ..model import SurfaceGuidedMassSystem


class SpecialForce(Force):
    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        return np.zeros((3,))
