from .surface import Surface

import numpy as np


class Sphere(Surface):
    plimits = [
        (0.0, 2*np.pi),   # u
        (-np.pi, np.pi),  # v
    ]

    def __init__(self, R=1.0):
        self.R = R

    def eval(self, u, v):
        sinv = np.sin(v)
        cosv = np.cos(v)

        sinu = np.sin(u)
        cosu = np.cos(u)
        x = self.R * sinv * cosu
        y = self.R * sinv * sinu
        z = - self.R * cosv

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