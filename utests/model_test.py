from gsurface import SurfaceGuidedMassSystem, Solid, EllipticParaboloid, Gravity, ViscousFriction, SpringForce

import numpy as np

from gsurface.tools import nprand

import unittest

class TestModel(unittest.TestCase):
    def test_model(self):
        np.testing.assert_array_less(
            SurfaceGuidedMassSystem(
                surface=EllipticParaboloid(1.0, 2.0),
                s0=nprand((4,)),
                solid=1.0,
                forces=[
                    Gravity(1.0, [0, 0, -10.0]),
                    SpringForce(1.0, [0.0, 0.0, 0.0]),
                    ViscousFriction(2.0),
                ],
            ).solve(time=np.linspace(0, 20, 1000))[-1,:],
            1e-5*np.ones((4,))
        )


if __name__ == '__main__':
    unittest.main()