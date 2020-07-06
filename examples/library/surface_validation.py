import numpy as np

from surface_guided_sim.surface import Surface, Sphere, Plan, Tore, EggBox
from surface_guided_sim.surface.misc import check_library_surfaces


surface = Sphere()

print(surface.check_verbose())

# check library
check_library_surfaces()