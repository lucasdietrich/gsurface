import numpy as np
import pprint

from surface_guided_sim.forces import Force, NoForce, Gravity, ForceFunction, ForceSum

h = ForceFunction(lambda u, v, t, S, J: np.array([0.0, 0.0, 0.1*t]))
g1 = Gravity(np.array([0.0, 0.0, 1.0]))
g2 = Gravity(np.array([0.0, -1.0, 1.0]))
g3 = Gravity(np.array([-2.0, -1.0, 1.0]))

s = g1 + g2 + h + g3

pprint.pprint(s)

print(s.eval(0, 0, 3, np.array([]), np.array([])))
