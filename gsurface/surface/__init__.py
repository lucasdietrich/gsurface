from .catenoid import Catenoid
from .conicalcorner import ConicalCorner
from .cylinder import Cylinder
from gsurface.surface.consistency.diff import get_diff_surface_errors
from .eggbox import EggBox
from .paraboloid import EllipticParaboloid, HyperbolicParaboloid
from .plan import Plan
from .sphere import Sphere
from .tore import Tore

__surfaces__ = [Tore, Plan, Sphere, EggBox, Catenoid, ConicalCorner, EllipticParaboloid, HyperbolicParaboloid, Cylinder]
