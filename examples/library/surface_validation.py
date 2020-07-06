import numpy as np

from surface_guided_sim.surface import Surface, Sphere, Plan, Tore, EggBox

surface = Sphere()

print(surface.check_verbose())

# invalid surface check


class InvalidSurface(Surface):
    def eval(self, u: float, v: float) -> np.ndarray:
        exp = np.exp(v)

        return self.buildevalreturn(
            x=u,
            y=v,
            z=u*exp,
            dux=1.01, # 1
            duz=exp,
            dvy=1,
            dvz=u*exp,
            duvz=exp,
            dvvz=u*u*exp # u*exp
        )

print(InvalidSurface().check_verbose())