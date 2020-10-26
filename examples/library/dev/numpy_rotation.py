# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html

import numpy as np

from scipy.spatial.transform import Rotation as R

n = np.array([1, 0, 0])

print(n)

# rotation arround x = 0.0, y = np.pi/4, z = np.pi/8
r = R.from_rotvec([0.0, np.pi/4, np.pi/8]).as_matrix()
print(r)

print(n @ r)