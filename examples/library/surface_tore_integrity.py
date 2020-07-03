from scipy.optimize import check_grad

from surface_guided_sim.surface.tore import Tore

from surface_guided_sim.misc import AverageMinMax

import numpy as np

angle = np.linspace(0, 2*np.pi, 10)

tore = Tore(0.5, 1.0)

tolerance = 1e-7

amm = AverageMinMax()

print("dS")
for X in (0, 1, 2): # x, y, z
    # check grad Sx
    def func(x):
        return tore.position(x[0], x[1])[X]

    def grad(x):
        return tore.SJH(x[0], x[1])[3 + 2 * X:5 + 2 * X]

    for u in angle:
        for v in angle:
            ret = check_grad(func, grad, np.array([u, v]))
            amm.add(ret)

    print(X, amm.max <= tolerance)

    amm.clear()

print("ddS")
for X in (0, 1, 2): # x, y, z
    for p1 in (0, 1): # partial u, v
        for p2 in (0, 1): # partial u, v
            # todo finish

            # check grad Sx
            def func(x):
                return tore.position(x[0], x[1])[3 + 2 * X + p1, 3 + 2 * X + p1 + 2]

            def grad(x):
                return tore.SJH(x[0], x[1])[3 + 2 * X:5 + 2 * X]

            for u in angle:
                for v in angle:
                    ret = check_grad(func, grad, np.array([u, v]))
                    amm.add(ret)

            print(X, amm.max <= tolerance)

            amm.clear()