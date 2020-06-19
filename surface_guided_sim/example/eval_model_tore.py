from surface_guided_sim.model_tore import *

import numpy as np

tore = SurfaceTore(0.5, 1.0)

sim = SurfaceGuidedFallSystem(tore)

e = tore.eval(1.0, 1.0)

print(e)

print(tore.eval(1.0, 1.0, pos_only=True))

print(sim.jacobian(tore.eval(1.0, 1.0)))
print(sim.hessian(tore.eval(1.0, 1.0), 0))
print(sim.hessian(tore.eval(1.0, 1.0), 1))
print(sim.hessian(tore.eval(1.0, 1.0), 2))