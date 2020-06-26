from surface_guided_sim.model import Surface
import numpy as np


class SurfaceTore(Surface):
    def __init__(self, r=0.5, R=1.0):
        self.r = r
        self.R = 1.0

    def eval(self, u, v):
        Rrcos = self.R + self.r * np.cos(v)

        x = Rrcos * np.cos(u)
        y = Rrcos * np.sin(u)
        z = self.r * np.sin(v)

        return np.array([x, y, z])

    def eval_all(self, u, v):
        x, y, z = self.eval(u, v)

        dux = -y
        dvx = -self.r*np.sin(v)*np.cos(u)

        duy = x
        dvy = -self.r*np.sin(v)*np.sin(u)

        duz = 0
        dvz = self.r*np.cos(v)

        duux = -x
        duvx = -dvy
        dvvx = -dvz*np.cos(u)

        duuy = -y
        duvy = -dvx
        dvvy = -dvz*np.sin(u)

        duuz = 0
        duvz = 0
        dvvz = -z

        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])