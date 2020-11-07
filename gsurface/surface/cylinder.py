import numpy as np

from .surface import Surface, SJH


class Cylinder(Surface):
    __repr_str__ = "(R={R:.2f})"

    def __init__(self, R: float = 1.0, **kargs):
        self.R = R

        super(Cylinder, self).__init__(
            plimits=np.array([
                [0.0, 2*np.pi],
                [0.0, 1.0]
            ])
        )

    def _definition(self, u: float, v: float) -> SJH:
        Rcosu = self.R*np.cos(u)
        Rsinu = self.R*np.sin(u)

        return self.buildMetric(
            x=Rcosu,
            y=Rsinu,
            z=v,

            dux=-Rsinu,
            duy=Rcosu,
            duz=0,

            dvx=0,
            dvy=0,
            dvz=1,

            duux=-Rcosu,
            duuy=-Rsinu,
        )
