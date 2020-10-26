import numpy as np

from .force import Force
from .friction import CenterDirectedViscousFriction
from .spring import SpringForce, LengthedSpringForce


def SpringDampingForce(stiffness: float = 1.0, mu: float = 1.0, clip: np.ndarray = None, l0: float = 0.0) -> Force:
    if clip is None:
        clip = np.zeros((3,))

    if l0 == 0.0:
        spring_force = SpringForce(stiffness, clip)
    else:
        spring_force = LengthedSpringForce(stiffness, clip, l0)

    viscous_force = CenterDirectedViscousFriction(mu, clip)

    return spring_force + viscous_force

