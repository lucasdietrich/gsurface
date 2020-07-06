from .surface import Surface

from .tore import Tore
from .plan import Plan
from .sphere import Sphere
from .eggbox import EggBox
from .catenoid import Catenoid

from .diff import get_diff_surface_errors

__surfaces__ = [Tore, Plan, Sphere, EggBox, Catenoid]
