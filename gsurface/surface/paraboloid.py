from .surface import Surface, np, SJH


# https://en.wikipedia.org/wiki/Paraboloid
class Paraboloid(Surface):
    def __init__(self, a: float = 1.0, b: float = 1.0):
        assert a and b

        self.a = a
        self.b = b

        self.inva2 = pow(a, -2)
        self.invb2 = pow(b, -2)

    def _definition(self, u: float, v: float) -> SJH:
        return self.buildMetric(
            x=u,
            y=v,
            z=u**2 * self.inva2 + v**2 * self.invb2,

            dux=1.0,
            dvy=1.0,
            duz=2*u*self.inva2,
            dvz=2*v*self.invb2,

            duuz=2*self.inva2,
            dvvz=2*self.invb2,
        )
