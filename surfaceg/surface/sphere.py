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

        dvx = R * cosu * cosv
        dvy = R * sinu * cosv

        return self.buildevalreturn(
            x=x,
            y=y,
            z=z,

            dux=-y,
            duy=x,

            dvx=dvx,
            dvy=dvy,
            dvz=R*sinv,

            duux=-x,
            duuy=-y,

            duvx=-dvy,
            duvy=dvx,

            dvvx=-x,
            dvvy=-y,
            dvvz=-z,
        )

