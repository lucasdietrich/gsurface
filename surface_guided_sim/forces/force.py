from __future__ import annotations

import numpy as np

from typing import Iterable, Callable, Union, Type

ForceEvalType = Callable[
    [np.ndarray, np.ndarray, float, np.ndarray, np.ndarray],
    np.ndarray
]

import abc


class Force(abc.ABC):
    @abc.abstractmethod
    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        raise NotImplementedError()

    def __call__(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None):
        return self.eval(w, dw, t, s, j)

    def __radd__(self, other: Union[ForceSum, Iterable[Force]]) -> ForceSum:
        return self + other

    def __add__(self, other: Union[Force, ForceSum, Iterable[Force]]) -> ForceSum:
        return ForceSum(other).append(self)

    def __repr__(self):
        return "{0}".format(self.__class__.__name__)


class ForceFunction(Force):
    def __init__(self, function: ForceEvalType):
        self.function = function

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        return self.function(w, dw, t, s, s)


class NoForce(Force):
    def __init__(self):
        self.force = np.zeros((3, ))

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        return self.force


class ForceSum(Force):
    def __init__(self, forces: Union[Force, ForceSum, Iterable[Force]] = None):
        self.forces = []

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

    def eval(self, w: np.ndarray, dw: np.ndarray, t: float, s: np.ndarray = None, j: np.ndarray = None) -> np.ndarray:
        return np.sum(
            force(w, dw, t, s, j) for force in self.forces
        )

    def __repr__(self):
        return super(ForceSum, self).__repr__() + self.forces.__repr__()


