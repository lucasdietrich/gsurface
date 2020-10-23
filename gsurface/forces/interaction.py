import numpy as np

from .force import Force
from ..model import SurfaceGuidedMassSystem

from ..types import ModelEvalState

from typing import List, Iterable, Tuple

import abc


class Interaction(abc.ABC):
    def __init__(self, models: List[SurfaceGuidedMassSystem]):
        assert len(models) == 2  # an interaction is between 2 systems

        self.models = models

    @abc.abstractmethod
    def eval(self, M1: ModelEvalState, M2: ModelEvalState) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}"


class SpringInteraction(Interaction):
    def __init__(self, models: List[SurfaceGuidedMassSystem], stiffness: float = 1.0):
        self.stiffness = stiffness

        super(SpringInteraction, self).__init__(models)

    def _force(self, M1: ModelEvalState, M2: ModelEvalState) -> np.ndarray:
        return -self.stiffness * (M1.S - M2.S)

    def eval(self, M1: ModelEvalState, M2: ModelEvalState) -> Tuple[np.ndarray, np.ndarray]:
        F1 = self._force(M1, M2)

        return F1, -F1


# todo add reverse method

# todo create general class that work on all other interacted methods

class OneSideSpringInteraction(SpringInteraction):
    def __init__(self, models: List[SurfaceGuidedMassSystem], stiffness: float = 1.0):
        """
        First model change second model behaviour but its own behaviour isn't altered

        :param models:
        :param stiffness:
        """
        super().__init__(models, stiffness)

    def eval(self, M1: ModelEvalState, M2: ModelEvalState) -> Tuple[np.ndarray, np.ndarray]:
        return np.zeros((3,)), - self._force(M1, M2)
