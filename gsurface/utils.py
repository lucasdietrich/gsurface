from typing import Tuple

import numpy as np


def direction(V: np.ndarray) -> np.ndarray:
    """
    Return the direction of the vector V
        if V is [0 0 0], return [0 0 0]

    Args:
        V: vector

    Returns: direction of V

    """
    norm = np.linalg.norm(V)

    if norm == 0:
        return np.zeros((3,))
    else:
        return V / norm


def speed(J: np.ndarray, dw: np.ndarray) -> np.ndarray:
    """
    Calculate solid speed for parametric speed dw and surface jacobian J

    Args:
        J: Jacobian
        dw: parametric speed

    Returns: local solid speed

    """
    return J @ dw.T


def distance(dest: np.ndarray, source: np.ndarray = None) -> Tuple[np.ndarray, float]:
    """
    Return vectorial distance from O to Q and its length

    distance(dist, source) is equivalent to distance(dist - source)

    Args:
        dest: destination
        source: source

    Returns: vectorial distance, scalar distance
    """
    if source is None:
        source = np.zeros((3,))

    v = dest - source
    vnorm = np.linalg.norm(v)

    return v, vnorm
