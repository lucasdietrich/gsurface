import abc

import numpy as np

from ..serialize.interface import SerializableInterface
from ..types import SJH


class TransformationStrategy(abc.ABC, SerializableInterface):
    def __init__(self, D: np.ndarray, M: np.ndarray):
        self.D = D
        self.M = M

    @abc.abstractmethod
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        raise NotImplementedError

    def __repr__(self):
        return "[{0}]".format(self.__class__.__name__[:-22])  # 22 for "TransformationStrategy"


class NoTransformationStrategy(TransformationStrategy):
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return S, J, H

    def __repr__(self):
        return ""


class ShiftTransformationStrategy(TransformationStrategy):
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return self.D + S, J, H


class RotTransformationStrategy(TransformationStrategy):
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        S = np.dot(self.M, S)
        J = np.dot(self.M, J)

        for i in range(2):
            for j in range(2):
                H[:,i,j] = np.dot(self.M, H[:,i,j])

        return S, J, H


class RotShiftTransformationStrategy(ShiftTransformationStrategy, RotTransformationStrategy):
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return ShiftTransformationStrategy.apply(
            self,
            *RotTransformationStrategy.apply(self, S, J, H)
        )


def GetTransformationStrategy(D: np.ndarray = None, M: np.ndarray = None) -> TransformationStrategy:
    eye = np.eye(3)

    if D is None:
        D = np.zeros((3,))

    if M is None:
        M = eye

    shift = np.any(D)
    rot = np.any(eye - M)

    if shift:
        if rot:
            return RotShiftTransformationStrategy(D, M)
        else:
            return ShiftTransformationStrategy(D, M)
    else:
        if rot:
            return RotTransformationStrategy(D, M)
        else:
            return NoTransformationStrategy(D, M)
