from typing import Callable

import numpy as np


# retourne une itération de la méthode de résolution d'équations différentielles de type ODE
# selon la méthode de Runge-Kutta : https://fr.wikipedia.org/wiki/M%C3%A9thodes_de_Runge-Kutta
# derivs fonction dérivée du modèle à l'état s en x
# s état du système à évaluer
# x valeur à laquelle évaluer le système
# variation élémentaire à évaluer
#
# s[x + dx] = s + rk4_ds(derivs, s, x, dx)
def rk4_ds(
        derivs: Callable[[np.ndarray, float], np.ndarray],
        s: np.ndarray,
        x: float,
        dx: float
) -> np.ndarray:
    ds1 = derivs(s, x)*dx
    ds2 = derivs(s + ds1 / 2, x + dx / 2)*dx
    ds3 = derivs(s + ds2 / 2, x + dx / 2)*dx
    ds4 = derivs(s + ds3, x + dx)*dx

    ds = (ds1 + ds4)/6 + (ds2 + ds3)/3

    return ds


# méthode de résolution d'équations différentielles de type ODE
# selon la méthode de Runge-Kutta : https://fr.wikipedia.org/wiki/M%C3%A9thodes_de_Runge-Kutta
# derivs fonction dérivée du modèle à l'état s en x
# s0, état initial du système
# valeurs auxquels évaluer le système
# retourne l'évolution du système s au cours de la variable x
def rk4(
        derivs: Callable[[np.ndarray, float], np.ndarray],
        s0: np.ndarray,
        x: np.ndarray
) -> np.ndarray:
    s = np.zeros(shape=(
        x.shape[0],
        *s0.shape
    ))
    s[0] = s0
    si = np.copy(s0)
    for i in range(0, len(x) - 1):
        xi = x[i]
        dx = x[i + 1] - xi
        ds = rk4_ds(derivs, si, xi, dx)
        si = s[i + 1] = si + ds

    return s
