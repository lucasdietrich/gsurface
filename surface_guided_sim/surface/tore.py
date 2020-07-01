from surface_guided_sim.model import Surface
import numpy as np


class SurfaceTore(Surface):
    def __init__(self, r=0.5, R=1.0):
        self.r = r
        self.R = 1.0

    def eval(self, u, v):
        Rrcos = self.R + self.r * np.sin(v)

        x = Rrcos * np.cos(u)
        y = Rrcos * np.sin(u)
        z = - self.r * np.cos(v)

        return np.array([x, y, z])

    def eval_all(self, u, v):
        x, y, z = self.eval(u, v)

        dux = -y
        duy = x
        duz = 0

        dvx = self.r*np.cos(u)*np.cos(v)
        dvy = self.r*np.sin(u)*np.cos(v)
        dvz = self.r*np.sin(v)

        duux = -x
        duuy = -y
        duuz = 0

        duvx = -dvy
        duvy = dvx
        duvz = 0

        dvvx = -dvz*np.cos(u)
        dvvy = -dvz*np.sin(u)
        dvvz = -z

        return np.array([
            x, y, z,
            dux, dvx, duy, dvy, duz, dvz,
            duux, duvx, dvvx, duuy, duvy, dvvy, duuz, duvz, dvvz
        ])