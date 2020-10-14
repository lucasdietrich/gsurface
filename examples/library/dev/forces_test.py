import numpy as np
import pprint

from gsurface.forces import Force, NoForce, Gravity, ForceFunction, ForceSum

h = ForceFunction(lambda u, v, t, S, J: np.array([0.0, 0.0, 0.1*t]))
g1 = Gravity(1.0, np.array([0.0, 0.0, 1.0]))
g2 = Gravity(1.0, np.array([0.0, -1.0, 1.0]))
g3 = Gravity(1.0, np.array([-2.0, -1.0, 1.0]))

s = g1 + g2 + h + g3

pprint.pprint(s)

print(s.eval(np.array([0, 0]), np.array([0, 0]), 3, np.array([]), np.array([])))
