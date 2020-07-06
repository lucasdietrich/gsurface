from surface_guided_sim.surface import Surface

import numpy as np


class ConicalCorner(Surface):
    __repr_str__ = "(k={k:.2f}, a={a:.2f})"

    plimits = np.array([
        [-2.0, 2.0],  # u lims
        [0, 2*np.pi]   # v lims
    ])

    def __init__(self, k:float = 1.0, a:float = 1.0):
        """
        Coin Conique
            https://mathcurve.com/surfaces/coinconic/coinconic.shtml
        :param k:
        :param a:
        """
        self.k = k
        self.a = a

    def eval(self, u: float, v: float) -> np.ndarray:
        k, a = self.k, self.a

        cosv = np.cos(v)
        sinv = np.sin(v)

        return self.buildevalreturn(
            x=u,
            y=k*u*cosv,
            z=k*a*sinv,

            dux=1,
            duy=k*cosv,

            dvy=-k*u*sinv,
            dvz=k*a*cosv,

            duvy=-k*sinv,

            dvvy=-k*u*cosv,
            dvvz=-a*k*sinv
        )


