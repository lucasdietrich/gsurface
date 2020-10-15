# test to synchronise two ODE systems
import numpy as np

from ode.system import ODESystem


class Sys(ODESystem):
    def __init__(self, a, s0: float):
        self.a = a
        super(Sys, self).__init__(np.array([s0]))

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        return np.array([-self.a/(t**2+self.a)*t])


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sys = Sys(4.0, 10.0)
    sys2 = Sys(2, 10.0)

    time = np.linspace(0, 1000, 1000)

    data = sys.solve(time)
    data2 = sys2.solve(time)

    plt.figure(1)
    plt.plot(time, data)
    plt.plot(time, data2)
    plt.grid(True)
    plt.show()

