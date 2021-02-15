import abc

import numpy as np
from ode.solver import rk4
from scipy.integrate import odeint


class ODESystem(abc.ABC):
    def __init__(self, s0: np.ndarray):
        """
        Represent a ODE system as s(t + dt) = s(t) + ODESystem._derivs(self, s(t), t)

        Where s is the state of the system :
        - Is usually a 1D vector
        - But can be a matrix if _derivs is well defined

        _derivs stands for derivative of s (prrotected method)

        state should have the same shape all over the simulation

        :param s0: Initial state of the system s0 = s(t0)
        """
        self.s0: np.ndarray = s0

    @abc.abstractmethod
    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        """
        Compute the derivative of s at time t

        :param s: current state s(t)
        :param t: current time
        :return: Derivative of s : ds/dt (t)
        """
        raise NotImplementedError()

    def solve(self, time: np.ndarray, solver=None, **kargs) -> np.ndarray:
        """
        Solve the system for the time linspace time using odeint from scipy.solver
        :param time: time linspace
        :param solver: solver lib/function
        :param kargs: additional parameters
        :return: all states of s in time t
        """
        if solver is None:
            solver = odeint

        return solver(self._derivs, self.s0, time, **kargs)

    def solve_rk4(self, time: np.ndarray) -> np.ndarray:
        """
        Solve the system for the time linspace time using rk4 from ode.solver

        :param time: time linspace
        :return: all states of s in time t
        """
        return self.solve(time, rk4)

    def build_null_s0(self, n: int):
        return np.zeros((n,))