from gsurface.surface import Tore, Plan, Sphere
from gsurface.model import SurfaceGuidedMassSystem
from gsurface.forces import SpringForce, ViscousFriction, Gravity

from scipy.integrate import odeint

from time import time

import numpy as np

tore = Tore(0.5, 1.0)

model = SurfaceGuidedMassSystem(
    surface=tore,
    s0=np.array([1.0, 1.0, 1.0, 1.0]),
    m=1.0,
    forces=[
        SpringForce(1.0, np.array([0.0, 0.0, 0.0])),
        ViscousFriction(0.01),
        Gravity(1.0, np.array([0.0, 0.0, -1.0]))
    ]
)

T = np.linspace(0, 100, 100000)

begin = time()
data = model.solve(T, solver=odeint)
end = time()

delta = end - begin

print(f"Time : {delta:.3f} s")