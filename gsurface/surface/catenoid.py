from .surface import Surface, np, SJH


class Catenoid(Surface):
    plimits = np.array([
        [-2.0, 2.0],  # u lims
        [0, 2*np.pi]   # v lims
    ])

    __repr_str__ = "(a={a:.2f})"

    def __init__(self, a: float = 1.0):
        """
        Catenoid:
            https://mathcurve.com/surfaces/catenoid/catenoid.shtml

        :param a:
        """
        self.a = a

    def _definition(self, u: float, v: float) -> SJH:

        chu = np.cosh(u)
        shu = np.sinh(u)
        cosv = np.cos(v)
        sinv = np.sin(v)

        a = self.a

        return self.buildMetric(
            x=a*chu*cosv,
            y=a*chu*sinv,
            z=a*u,

            dux=a*shu*cosv,
            duy=a*shu*sinv,
            duz=a,

            dvx=-a*chu*sinv,
            dvy=a*chu*cosv,

            duux=a*chu*cosv,
            duuy=a*chu*sinv,

            duvx=-a*shu*sinv,
            duvy=a*shu*cosv,

            dvvx=-a*chu*cosv,
            dvvy=-a*chu*sinv,
        )