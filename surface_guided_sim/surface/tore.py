from .surface import Surface

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

    def eval(self, u, v):
        sinv = np.sin(v)
        cosv = np.cos(v)

        sinu = np.sin(u)
        cosu = np.cos(u)

        Rrcos = self.R + self.r * sinv

        x = Rrcos * cosu
        y = Rrcos * sinu
        z = - self.r * cosv

        dux = -y
        duy = x
        duz = 0

        dvx = self.r*cosu*cosv
        dvy = self.r*sinu*cosv
        dvz = self.r*sinv

        duux = -x
        duuy = -y
        duuz = 0

        duvx = -dvy
        duvy = dvx
        duvz = 0

        dvvx = -dvz*cosu
        dvvy = -dvz*sinu
        dvvz = -z

        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])