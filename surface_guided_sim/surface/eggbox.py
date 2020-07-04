from .surface import Surface

import numpy as np

from typing import Callable


class EggBox(Surface):
    def __init__(self, R: float = 1.0, a: float = 1.0, b: float = 1.0):
        self.R = R
        self.a = a
        self.b = b

    def eval(self, u: float, v: float) -> np.ndarray:
        R, a, b = self.R, self.a, self.b

        cosau = np.cos(a*u)
        sinau = np.sin(a*u)
        cosbv = np.cos(b*v)
        sinbv = np.sin(b*v)

        return Surface.buildevalreturn(
            x=u,
            y=v,
            z=R*cosau*cosbv,

            dux=1,
            duy=0,
            duz=-R*a*sinau*cosbv,

            dvx=0,
            dvy=1,
            dvz=-R*b*sinbv*cosau,

            duux=0,
            duuy=0,
            duuz=-R*a**2*cosau*cosbv,

            duvx=0,
            duvy=0,
            duvz=R*a*b*sinau*sinbv,

            dvvx=0,
            dvvy=0,
            dvvz=-R*b**2*cosau*cosbv
        )
