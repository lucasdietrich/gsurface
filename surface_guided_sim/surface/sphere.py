from .surface import Surface

import numpy as np


class Sphere(Surface):
    __repr_str__ = "(R={R:.2f})"

    plimits = np.array([
        [0.0, 2*np.pi],   # u
        [-np.pi, np.pi],  # v
    ])

    def __init__(self, R=1.0):
        self.R = R

    def eval(self, u, v):
        sinv = np.sin(v)
        cosv = np.cos(v)

        sinu = np.sin(u)
        cosu = np.cos(u)

        R = self.R

        x = R * cosu * sinv
        y = R * sinu * sinv
        z = - R * cosv

        dux = -y
        duy = x
        duz = 0.0

        dvx = R*cosu*cosv
        dvy = R*sinu*cosv
        dvz = R*sinv

        duux = -x
        duuy = -y
        duuz = 0.0

        duvx = -dvy
        duvy = dvx
        duvz = 0.0

        dvvx = -duy
        dvvy = -y
        dvvz = -z

        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])