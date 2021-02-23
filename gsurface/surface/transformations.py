import abc

import numpy as np

from ..serialize.interface import SerializableInterface
from ..types import SJH

EYE = np.eye(3)


class TransformationStrategy(abc.ABC, SerializableInterface):
    TRANSLATION = 0
    ROTATION = 0

    @abc.abstractmethod
    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        raise NotImplementedError

    def __repr__(self):
        return "[{0}]".format(self.__class__.__name__[:-22])  # 22 for "TransformationStrategy"


class NoTransformationStrategy(TransformationStrategy):
    TRANSLATION = 0
    ROTATION = 0

    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return S, J, H

    def __repr__(self):
        return ""


class ShiftTransformationStrategy(TransformationStrategy):
    TRANSLATION = 1
    ROTATION = 0

    def __init__(self, D: np.ndarray):
        self.D = D

    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return self.D + S, J, H


class RotTransformationStrategy(TransformationStrategy):
    TRANSLATION = 0
    ROTATION = 1

    def __init__(self, M: np.ndarray):
        self.M = M

    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        S = np.dot(self.M, S)
        J = np.dot(self.M, J)

        for i, j in [(0, 0), (0, 1), (1, 1)]:
            H[:, i, j] = np.dot(self.M, H[:, i, j])
        H[:, 1, 0] = H[:, 0, 1]

        return S, J, H


class RotShiftTransformationStrategy(ShiftTransformationStrategy, RotTransformationStrategy):
    TRANSLATION = 1
    ROTATION = 1

    def __init__(self, D: np.ndarray, M: np.ndarray):
        ShiftTransformationStrategy.__init__(self, D)
        RotTransformationStrategy.__init__(self, M)

    def apply(self, S: np.ndarray, J: np.ndarray, H: np.ndarray) -> SJH:
        return ShiftTransformationStrategy.apply(
            self,
            *RotTransformationStrategy.apply(self, S, J, H)
        )


def UpdateTransformationStrategy(prev: TransformationStrategy, D: np.ndarray = None, M: np.ndarray = None) -> TransformationStrategy:
    defaultD, defaultM = None, None

    if isinstance(prev, RotTransformationStrategy):
        defaultM = prev.M
    elif isinstance(prev, ShiftTransformationStrategy):
        defaultD = prev.D
    elif isinstance(prev, RotShiftTransformationStrategy):
        defaultM, defaultD = prev.M, prev.D

    if D is None:
        D = defaultD

    if M is None:
        M = defaultM

    return GetTransformationStrategy(D, M)


def GetTransformationStrategy(D: np.ndarray = None, M: np.ndarray = None) -> TransformationStrategy:
    if D is None:
        D = np.zeros((3,))

    if M is None:
        M = np.copy(EYE)

    shift = np.any(D)
    rot = np.any(EYE - M)

    if shift:
        if rot:
            return RotShiftTransformationStrategy(D, M)
        else:
            return ShiftTransformationStrategy(D)
    else:
        if rot:
            return RotTransformationStrategy(M)
        else:
            return NoTransformationStrategy()
