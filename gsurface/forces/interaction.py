import abc
from typing import List, Tuple

import numpy as np

from gsurface import utils
from ..model import SurfaceGuidedMassSystem
from ..types import ModelEvalState

from gsurface.serialize import SerializableInterface


# an interaction is between 2 models
class Interaction(abc.ABC, SerializableInterface):
    @abc.abstractmethod
    def _force(self, M1: ModelEvalState, M2: ModelEvalState) -> np.ndarray:
        raise NotImplementedError

    def eval(self, M1: ModelEvalState, M2: ModelEvalState) -> Tuple[np.ndarray, np.ndarray]:
        F1 = self._force(M1, M2)

        return F1, -F1

    def __repr__(self):
        return f"{self.__class__.__name__}"

class SpringInteraction(Interaction):
    def __init__(self, stiffness: float = 1.0, **kargs):
        self.stiffness = stiffness

    def _force(self, M1: ModelEvalState, M2: ModelEvalState) -> np.ndarray:
        return -self.stiffness * (M1.S - M2.S)


class SpringDampingInteraction(Interaction):
    def __init__(self, stiffness: float = 1.0, mu: float = 1.0, l0: float = 1.0, **kargs):
        self.stiffness = stiffness
        self.mu = mu
        self.l0 = l0

    def _force(self, M1: ModelEvalState, M2: ModelEvalState) -> np.ndarray:
        DS, L = utils.distance(M1.S, M2.S)

        if not L:
            return np.zeros((3,))

        direction = DS / L

        V = M1.V - M2.V

        V, Vnorm = utils.distance(M1.V, M2.V)

        alpha = np.dot(V, direction)

        return -self.stiffness * (L - self.l0) * direction - self.mu * alpha * Vnorm * direction


# todo add reverse method

# todo create general class that work on all other interacted methods

class OneSideSpringInteraction(SpringInteraction):
    def __init__(self, stiffness: float = 1.0, **kargs):
        """
        First model change second model behaviour but its own behaviour isn't altered

        :param models:
        :param stiffness:
        """
        super().__init__(stiffness)

    def eval(self, M1: ModelEvalState, M2: ModelEvalState) -> Tuple[np.ndarray, np.ndarray]:
        return np.zeros((3,)), - super(OneSideSpringInteraction, self).eval(M1, M2)[0]
