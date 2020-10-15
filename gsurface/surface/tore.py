from .surface import Surface, SJH

import numpy as np


class Tore(Surface):
    __repr_str__ = "(r={r:.2f}, R={R:.2f})"

    plimits = np.array([
            [0.0, 2*np.pi],
            [-np.pi, np.pi]
        ])

    def __init__(self, r=0.5, R=1.0):
        self.r = r
        self.R = R

    def _definition(self, u, v) -> SJH:
        sinv = np.sin(v)
        cosv = np.cos(v)

        sinu = np.sin(u)
        cosu = np.cos(u)

        Rrcos = self.R + self.r * sinv

        x = Rrcos * cosu
        y = Rrcos * sinu
        z = - self.r * cosv

        dvx = self.r*cosu*cosv
        dvy = self.r*sinu*cosv
        dvz = self.r*sinv

        return self.buildMetric(
            x=x,
            y=y,
            z=z,

            dux=-y,
            duy=x,

            dvx=dvx,
            dvy=dvy,
            dvz=dvz,

            duux=-x,
            duuy=-y,

            duvx=-dvy,
            duvy=dvx,

            dvvx=-dvz*cosu,
            dvvy=-dvz*sinu,
            dvvz=-z,
        )
