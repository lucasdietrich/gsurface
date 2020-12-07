import numpy as np

from gsurface.forces import Gravity

v1 = np.array([1, 2, 3])
v2 = np.array([1.0, 2, 3])

g1 = Gravity(1.0, v1)
g2 = Gravity(1.0, v2)
