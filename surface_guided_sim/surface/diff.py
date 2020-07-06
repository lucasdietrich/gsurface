from surface_guided_sim.indexes import *

from surface_guided_sim.surface import Surface

import numpy as np

from scipy.optimize import check_grad

# check derivative of a function
# check the integrity of a surface class

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.check_grad.html


def surface_eval_grad_slice(index: int) -> slice:
    if index in (xi, yi, zi):
        duXi = 3 + 2*index
        dvXi = duXi + 1
        return slice(duXi, dvXi + 1)
    if index in (duxi, dvxi, duyi, dvyi, duzi, dvzi):
        X = (index - 3) // 2
        dwi = 1 - (index & 1)

        dudwXi = 9 + 3*X + dwi
        dvdwXi = dudwXi + 1

        return slice(dudwXi, dvdwXi + 1)
    else:
        raise AttributeError("index {0} doesn't have a surface defined gradient".format(index))


def build_function_eval(surface: Surface, index: int):
    def _(uv: np.ndarray) -> float:
        return surface.eval(uv[ui], uv[vi])[index]
    return _


def build_function_gradient(surface: Surface, index: int):
    slicing = surface_eval_grad_slice(index)

    def _(uv: np.ndarray) -> np.ndarray:
        return surface.eval(uv[ui], uv[vi])[slicing]
    return _


def get_diff_surface_errors(surface: Surface, U: np.ndarray, V: np.ndarray):
    indexes = duuxi
    err_matrix = np.zeros([
        indexes,
        U.shape[0],
        V.shape[0]
    ])
    functions = []

    for index in range(indexes):
        functions.append(
            (
                build_function_eval(surface, index),
                build_function_gradient(surface, index),
            )
        )

    for index in range(indexes):
        for i, u in enumerate(U):
            for j, v in enumerate(V):
                err_matrix[index, i, j] = check_grad(
                    *functions[index],
                    np.array([u, v])
                )

    return err_matrix
