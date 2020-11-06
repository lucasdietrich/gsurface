from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict

from gsurface.solid import SolidParameters

from gsurface.misc.serializable_interface import SerializableInterface

# graphes
#  https://fr.wikipedia.org/wiki/Th%C3%A9orie_des_graphes
#  https://fr.wikipedia.org/wiki/Lexique_de_la_th%C3%A9orie_des_graphes


@dataclass
class InteractionParameters:
    stiffness: float = 1000.0
    mu: float = 10.0
    l0: float = 1.0


GraphNodesType = List[SolidParameters]
VertexType = Tuple[int, int]
GraphVerticesType = Dict[VertexType, InteractionParameters]


# warning all subclasses need to modified SerializableInterface method if other parameters are nessesary to describe the model
class StructureGraph(SerializableInterface):
    def __init__(self, nodes: GraphNodesType = None, interactions: GraphVerticesType = None):
        if nodes is None:
            nodes = list()

        if interactions is None:
            interactions = dict()

        self.nodes: GraphNodesType = nodes
        self.interactions: GraphVerticesType = interactions

    def __repr__(self):
        return f"{self.__class__.__name__} : Nodes [{self.N}] vertices [{self.D}] connex [{self.isConnex()}] " \
               f"consistant [{self.isConsistant()}] fully constrainted [{self.isFullyConstrained()}]"

    # size of the structure (number of nodes)
    def getSize(self):
        return len(self.nodes)

    # degree of the structure (number of interactions)
    def getDegree(self):
        return len(self.interactions)

    N = property(getSize)
    D = property(getDegree)

    # does sense only if graph in connexe !
    # totally constraint graph has n (n - 1) / 2 interactions
    def isFullyConstrained(self):
        return self.D == self.maxInteractions()

    def maxInteractions(self) -> int:
        return self.N * (self.N - 1) // 2

    # determine if the graphe is connexe or not
    #  https://fr.wikipedia.org/wiki/Graphe_connexe
    #  implémentation of https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_profondeur
    # we explore the first node, if number of marked nodes isn't equal to number of nodes,
    # then the graph is not connexe
    def isConnex(self):
        assert self.getSize() > 1

        marked = []

        self._exploreNode(0, marked)

        return len(marked) == self.getSize()

    def _exploreNode(self, i: int, marked: List):
        marked.append(i)

        for k, l in self.interactions:
            neighbor = -1
            if i == k:
                neighbor = l
            elif i == l:
                neighbor = k

            if neighbor != -1 and neighbor not in marked:
                self._exploreNode(neighbor, marked)

    # size is minimum 2
    # degree is at least size - 1
    # all nodes are connected in a common structure/network
    def isConsistant(self):
        if self.getSize() < 2:
            return False  # not a network

        if self.getDegree() < self.getSize() - 1:
            return False  # not enough interactions to connect the networks

        return self.isConnex()

    def __getitem__(self, item: VertexType):
        return self.interactions[item]

    @staticmethod
    def genAllVertices(N: int):
        """
        Generate all vertices to define a connexe and fully constrained graph
            each Vertex is composed of type (Node i, Node j) where i < j
        :param N: Number of nodes
        :return: generator of Vertices : Iterable[Tuple[int, int]]
        """
        for i in range(N):
            for j in range(i + 1, N):
                yield i, j

    # manage dict[Tuple, Class] to list[(Tuple, Class)]
    def todict(self):
        d = super().todict()
        d["interactions"] = list(self.interactions.items())

        return d

    # manage list[(Tuple, Class)] to dict[Tuple, Class]
    @classmethod
    def fromdict(cls, d: dict):
        # rebuild from StructureGraph and not subclasses
        return StructureGraph(
            nodes=d["nodes"],
            interactions=d["interactions"]
        )


