import unittest

import numpy as np
import numpy.testing

from gsurface.forces.spring import SpringForce
from utests import Mock


class TestSpringForce(unittest.TestCase):
    def test_eval(self):
        stiffness = 10.0
        clip = np.array([1.0, 1.0, 1.0])
        numpy.testing.assert_array_equal(
            SpringForce(
                stiffness=stiffness,
                clip=clip
            ).eval(Mock.t(), -clip, Mock.V()),
            2*stiffness*np.ones((3,))
        )

    # do it with test suite
    def test_potential(self):
        pass


if __name__ == '__main__':
    unittest.main()