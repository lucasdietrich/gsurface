import numpy as np
from scipy.spatial.transform import Rotation

from gsurface.surface.transformations import RotTransformationStrategy, ShiftTransformationStrategy, NoTransformationStrategy, RotShiftTransformationStrategy
from gsurface.surface import Tore

tore = Tore(0.25, 1.0)

S, J, H = tore.eval(np.pi/4, np.pi/4)

M = Rotation.from_rotvec([1, 2, 3]).as_matrix()

transf = RotTransformationStrategy(M)

rS, rJ, rH = transf.apply(S, J, H)

print(S, rS)
print(J, rJ)
print(H, rH)