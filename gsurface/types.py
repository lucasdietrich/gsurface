from dataclasses import dataclass
from typing import Tuple

import numpy as np

SJH = Tuple[np.ndarray, np.ndarray, np.ndarray]


# classe d'état calculée pour un modèle de surface
@dataclass
class ModelEvalState:
    w: np.ndarray = None
    dw: np.ndarray = None
    S: np.ndarray = None
    J: np.ndarray = None
    H: np.ndarray = None

    iF: np.ndarray = np.zeros((3,0))
