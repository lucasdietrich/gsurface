from dataclasses import dataclass

import numpy as np


# classe d'état calculée pour un modèle de surface
@dataclass
class ModelEvalState:
    w: np.ndarray = None
    dw: np.ndarray = None
    S: np.ndarray = None
    J: np.ndarray = None
    H: np.ndarray = None

    iF: np.ndarray = np.zeros((3,0))
