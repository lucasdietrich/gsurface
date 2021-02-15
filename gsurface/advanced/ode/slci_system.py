from abc import ABC, abstractmethod
from typing import Iterable, Union

import numpy as np
from ode.solver import rk4_ds
from ode.system import ODESystem

# todo when SLCISystem.u(time) --> shape (2, 1, n)
# todo command depending of values x (state) and y (output)
# todo rendre la résolution itérable :
#  for state in system.until(time=10, value=23):
#       system.u = f(state)
#       plot(state)

LINES = 0
COLUMNS = 1


class SLCIsystem(ODESystem, ABC):
    def __init__(self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray, X0: np.ndarray):
        assert X0.shape[COLUMNS] == 1
        assert A.shape[LINES] == A.shape[COLUMNS] == B.shape[LINES] == C.shape[COLUMNS] == X0.shape[LINES]
        assert C.shape[LINES] == D.shape[LINES]  # == y.shape
        # assert self.u(0.0).shape[COLUMNS] == 1
        assert D.shape[COLUMNS] == B.shape[COLUMNS]  # == self.u(0.0).shape[LINES]

        self.ysize = C.shape[LINES]
        self.n = A.shape[LINES]

        super(SLCIsystem, self).__init__(s0=X0)

        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def eval_output(self, X: np.ndarray, t: float) -> np.ndarray:
        return np.dot(self.C, X) + np.dot(self.D, self.u(t, X))

    # recursion progrem when u call self.eval_output
    @abstractmethod
    def u(self, t: Union[float, Iterable[float]], X: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def solve(self, t: np.ndarray):
        Y = np.zeros(shape=(
            t.shape[0],
            self.ysize,
            1
        ))
        X = np.zeros(shape=(
            t.shape[0],
            *self.s0.shape
        ))
        X[0] = self.s0
        Y[0] = self.eval_output(X[0], t[0])

        xi = np.copy(self.s0)
        for i in range(0, len(t) - 1):
            ti = t[i]
            dt = t[i + 1] - ti
            dx = rk4_ds(self._derivs, xi, ti, dt)
            xi = X[i + 1] = xi + dx
            Y[i + 1] = self.eval_output(xi, ti)
        return Y, X

    def _derivs(self, X: np.ndarray, t: float):
        # self.Y = np.dot(self.C, X) + np.dot(self.D, self.u(t))
        return np.dot(self.A, X) + np.dot(self.B, self.u(t, X))

    def observability_matrix(self) -> np.ndarray:
        CA = self.C
        M = np.array([*CA])
        for i in range(1, self.n):
            CA = np.dot(CA, self.A)
            M = np.array([
                *M,
                *CA
            ])
        return M

    def controllability_matrix(self) -> np.ndarray:
        AB = self.B.transpose()
        M = np.array([*AB])

        AT = self.A.transpose()

        for i in range(1, self.n):
            AB = np.dot(AB, AT)
            M = np.array([
                *M,
                *AB
            ])
        return M.transpose()

    def observable(self) -> bool:
        return np.linalg.matrix_rank(self.observability_matrix()) == self.n

    def controllable(self) -> bool:
        return np.linalg.matrix_rank(self.controllability_matrix()) == self.n

