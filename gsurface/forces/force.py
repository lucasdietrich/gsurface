from __future__ import annotations

import abc

import numpy as np

from gsurface.types import ModelEvalState

from typing import Iterable, Callable, Union, List

from gsurface.misc.serializable_interface import SerializableInterface

# force eval function type : ForceEvalType(position(3), speed(3), time(1), surface diff(3), Hessian (3xH)) -> force(3)
ForceEvalType = Callable[
    [np.ndarray, np.ndarray, float, np.ndarray, np.ndarray],
    np.ndarray
]


class Force(abc.ABC, SerializableInterface):
    def evalM(self, t: float, M: ModelEvalState):
        return self.eval(M.w, M.dw, t, M.S, M.J)

    @abc.abstractmethod
    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        raise NotImplementedError()

    def __call__(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None):
        return self.eval(w, dw, t, S, J)

    def __radd__(self, other: Union[ForceSum, Iterable[Force]]) -> ForceSum:
        return self + other

    def __add__(self, other: Union[Force, ForceSum, Iterable[Force]]) -> ForceSum:
        return ForceSum(other).append(self)

    __repr_str__ = ""

    def __repr__(self):
        return (
            "{0} : " + self.__repr_str__
        ).format(self.__class__.__name__, **self.__dict__)


# https://fr.wikipedia.org/wiki/Force_conservative
class ConservativeForce(Force):
    @abc.abstractmethod
    def potential(self, t: float, S: np.ndarray) -> float:
        raise NotImplementedError()


class ForceFunction(Force):
    def __init__(self, function: ForceEvalType):
        self.function = function

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return self.function(w, dw, t, S, J)


class NoForce(Force):
    def __init__(self):
        self.force = np.zeros((3, ))

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return self.force


class ForceSum(Force):
    def __init__(self, forces: Union[Force, ForceSum, Iterable[Force]] = None, **kargs):
        if forces is None:
            forces = []

        self.forces: List[Force] = []

        self.append(forces)

        if len(self.forces) == 0:
            self.forces.append(NoForce())

    def append(self, other: Union[Force, ForceSum, Iterable[Force]]) -> ForceSum:
        if isinstance(other, Iterable):
            for force in other:
                self.forces.append(force)
        elif isinstance(other, ForceSum):
            self.append(other.forces)
        elif isinstance(other, Force):
            self.forces.append(other)
        else:
            raise AttributeError("other must be of type Union[Force, ForceSum, Iterable[Force]]")
        return self

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, S: np.ndarray = None, J: np.ndarray = None) -> np.ndarray:
        return np.sum(
            force(w, dw, t, S, J) for force in self.forces
        )

    def get_conservative_forces(self) -> Iterable[ConservativeForce]:
        for force in self.forces:
            if isinstance(force, ConservativeForce):
                yield force

    def __repr__(self):
        return super(ForceSum, self).__repr__() + self.forces.__repr__()
