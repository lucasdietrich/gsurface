import numpy as np

from .force import Force
from .friction import CenterDirectedViscousFriction
from .spring import SpringForce, LengthedSpringForce


# spring and damping in parallel, friction only apply in the direction S to clip
def SpringDampingForce(stiffness: float = 1.0, mu: float = 1.0, clip: np.ndarray = None, l0: float = 0.0) -> Force:
    if not l0:
        spring_force = SpringForce(stiffness, clip)
    else:
        spring_force = LengthedSpringForce(stiffness, clip, l0)

    viscous_force = CenterDirectedViscousFriction(mu, clip)

    return spring_force + viscous_force

