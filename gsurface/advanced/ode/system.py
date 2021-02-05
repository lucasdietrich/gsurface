from abc import ABC, abstractmethod

import numpy as np

from scipy.integrate import odeint


class ODESystem(ABC):
    def __init__(self, s0: np.ndarray):
        self.s0 = s0

    @abstractmethod
    def _derivs(self, S: np.ndarray, t: float):
        raise NotImplementedError()

    def solve(self, time: np.ndarray) -> np.ndarray:
        return odeint(self._derivs, self.s0, time)
