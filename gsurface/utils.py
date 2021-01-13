import numpy as np


def direction(V: np.ndarray) -> np.ndarray:
    """
    Return the direction of the vector V

    if V is [0 0 0], return [0 0 0]
    """
    norm = np.linalg.norm(V)

    if norm == 0:
        return np.zeros((3,))
    else:
        return V / norm