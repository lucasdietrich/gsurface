import random

import numpy as np

from gsurface.tools import nprand

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
    def s0() -> np.ndarray:
        return nprand((4,))

    @staticmethod
    def V() -> np.ndarray:
        return nprand((3,))

    @staticmethod
    def float() -> float:
        return random.random()
