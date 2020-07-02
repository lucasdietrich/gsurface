from scipy.integrate import odeint

import numpy as np

import abc


class ODESystem(abc.ABC):
    def __init__(self, s0: np.ndarray):
        self.s0: np.ndarray = s0

    @abc.abstractmethod
    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        raise NotImplementedError()

    def solve(self, time: np.ndarray):
        return odeint(self._derivs, self.s0, time)
