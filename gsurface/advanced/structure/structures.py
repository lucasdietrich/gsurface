import numpy as np

from .graph import StructureGraph, Solid, InteractionParameters


# Triangle structure as
# 3 nodes > 3 forces > fully constrained
# graph :
#     I
#  S --- S
#    \ / I
#   I V
#     S
# nodes orders:
# S0, S1
# S2
class TriangleStructure(StructureGraph):
    def __init__(self, totalMass: float = 1.0, stiffness: float = 1000.0, mu: float = 10.0, l0: float = 1.0, **kargs):
        self.totalMass = totalMass
        self.stiffness = stiffness
        self.mu = mu
        self.l0 = l0
        super(TriangleStructure, self).__init__(
            nodes=[Solid(totalMass / 3) for _ in range(3)],
            interactions={
                vertex: InteractionParameters(stiffness, mu, l0) for vertex in StructureGraph.genAllVertices(3)
            }
        )


# 4 wheels > 6 forces > fully constrained
# graph :
# W --- W
# | \ / |
# |  X  |
# | / \ |
# W --- W

# wheels order:
# W0, W1
# W2, W3
class CarStructure(StructureGraph):
    def __init__(self, totalMass: float = 1.0, ratio: float = 2, stiffness: float = 1000.0, mu: float = 10.0, l0: float = 1.0, **kargs):
        self.totalMass = totalMass
        self.stiffness = stiffness
        self.mu = mu
        self.l0 = l0

        # car dimensions
        self.ratio = ratio
        self.width = l0
        self.length = ratio * self.width
        self.diagonal = l0 * np.sqrt(1 + ratio**2)

        super(CarStructure, self).__init__(
            nodes=[Solid(totalMass / 4) for _ in range(4)],
            interactions={
                vertex: InteractionParameters(stiffness, mu, l0) for vertex in StructureGraph.genAllVertices(4)
            }
        )

        # fix lengthes
        self.interactions[(0, 2)].l0 = self.interactions[(1, 3)].l0 = self.length
        self.interactions[(0, 3)].l0 = self.interactions[(1, 2)].l0 = self.diagonal


class SnakeStructure(StructureGraph):
    def __init__(self, n: int = 4, totalMass: float = 1.0, stiffness: float = 1000.0, mu: float = 10.0, length: float = 1.0, **kargs):
        self.totalMass = totalMass
        self.stiffness = stiffness
        self.mu = mu
        self.n = int(n)
        self.length = length
        l0 = length / (self.n - 1)

        super(SnakeStructure, self).__init__(
            nodes=[Solid(totalMass / n) for _ in range(n)],
            interactions={
                (j, j + 1): InteractionParameters(stiffness, mu, l0) for j in range(n - 1)
            }
        )



class BowStructure(SnakeStructure):
    """
    Snake structure but first and last nodes are connected
    """
    def __init__(self, n: int = 4, totalMass: float = 1.0, stiffness: float = 1000.0, mu: float = 10.0, length: float = 1.0, **kargs):
        super(BowStructure, self).__init__(
            n=n,
            totalMass=totalMass,
            stiffness=stiffness,
            mu=mu,
            length=length
        )

        self.interactions[(0, n - 1)].l0 = length
