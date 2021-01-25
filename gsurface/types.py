from dataclasses import dataclass
from typing import Tuple

import numpy as np

TIME = float
POSITION = np.ndarray
HESSIAN = np.ndarray
JACOBIAN = np.ndarray
SPEED = np.ndarray
FORCE = np.ndarray

# S : Surface, J : Jacobian, H : [H_x, H_y, H_z] Hessians of S_x, S_y, S_z
SJH = Tuple[POSITION, JACOBIAN, HESSIAN]


# classe d'état calculée pour un modèle de surface
@dataclass
class ModelEvalState:
    w: np.ndarray = None
    dw: np.ndarray = None
    S: np.ndarray = None
    V: np.ndarray = None
    J: np.ndarray = None
    H: np.ndarray = None

    iF: np.ndarray = np.zeros((3, 0))
