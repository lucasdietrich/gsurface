from .surface import Surface, SJH

import numpy as np


class EggBox(Surface):
    __repr_str__ = "(R={R:.2f}, a={a:.2f}, a={b:.2f})"

    def __init__(self, R: float = 1.0, a: float = 1.0, b: float = 1.0):
        self.R = R
        self.a = a
        self.b = b

    def _definition(self, u: float, v: float) -> SJH:
        R, a, b = self.R, self.a, self.b

        cosau = np.cos(a*u)
        sinau = np.sin(a*u)
        cosbv = np.cos(b*v)
        sinbv = np.sin(b*v)

        return self.buildMetric(
            x=u,
            y=v,
            z=R*cosau*cosbv,

            dux=1,
            duz=-R*a*sinau*cosbv,

            dvy=1,
            dvz=-R*b*sinbv*cosau,

            duuz=-R*a**2*cosau*cosbv,

            duvz=R*a*b*sinau*sinbv,

            dvvz=-R*b**2*cosau*cosbv
        )
