from __future__ import annotations

from .graph import StructureGraph, InteractionEdge, GraphVerticesType, VertexType, GraphNodesType
from gsurface.solid import Solid

import numpy as np

from typing import List, Tuple, Dict


GraphPosNodesType = List[Tuple[Solid, np.ndarray]]


class ExplStructureGraph(StructureGraph):
    def __init__(self, nodes: GraphNodesType, positions: List[np.ndarray], interactions: GraphVerticesType = None):
        """
        Describe a structure of mass points by their position and the interactions between the nodes

        Comments :
            - Fully constrained structure

        Args:
            nodes:
            interactions: list of interactions between nodes (l0 are all ignored and recalculated)
        """
        super(ExplStructureGraph, self).__init__(
            nodes=nodes,
            interactions=interactions
        )
        self.positions = [np.array(pos) for pos in positions]

        for edge in self.genAllVertices(self.N):
            self[edge].l0 = np.linalg.norm(self.positions[edge[0]] - self.positions[edge[1]])

    def todict(self):
        d = super(ExplStructureGraph, self).todict().copy()

        print(d)

        d.update({
            "positions": self.positions
        })

        return d

    @classmethod
    def fromdict(cls, d: dict) -> ExplStructureGraph:
        # rebuild from StructureGraph and not subclasses
        return ExplStructureGraph(
            nodes=d["nodes"],
            positions=d["positions"],
            interactions={
                (na, nb): v for (na, nb), v in d["interactions"]
            }
        )