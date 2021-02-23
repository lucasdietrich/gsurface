import abc
from typing import Tuple

import numpy as np

from gsurface.advanced.ode.system import ODESystem
from gsurface.serialize.interface import SerializableInterface


class SurfaceGuidedBaseSystem(ODESystem, SerializableInterface, abc.ABC):
    @abc.abstractmethod
    def solutions(self, states: np.ndarray, time: np.ndarray):
        raise NotImplementedError()

    @abc.abstractmethod
    def dimension(self) -> Tuple[int, int, int]:
        raise NotImplementedError()
