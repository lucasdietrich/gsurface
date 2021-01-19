import random
from typing import Union, Iterable

import numpy as np


def nprand(shape: Union[int, Iterable[int]], lower: float = -1.0, upper: float = 1.0) -> np.ndarray:
    """
    Create a ndarray with a certain shape of random values

    Args:
        shape: e.g. (2, 2, 2) Mock Surface Hessians for example
        lower: lower boundary
        upper: upper boundary

    Returns: ndarray of random values

    """
    amplitude = upper - lower

    array = np.zeros(shape)

    for index, val in np.ndenumerate(array):
        array[index] = amplitude * random.random() + lower

    return array


class Mock:
    @staticmethod
    def w() -> np.ndarray:
        return nprand((2,))

    @staticmethod
    def dw() -> np.ndarray:
        return nprand((2,))

    @staticmethod
    def H() -> np.ndarray:
        return nprand((2, 2, 2))

    @staticmethod
    def J() -> np.ndarray:
        return nprand((3, 2))

    @staticmethod
    def S() -> np.ndarray:
        return nprand((3,))

    @staticmethod
    def t() -> float:
        return Mock.float()

    @staticmethod
    def float() -> float:
        return random.random()
