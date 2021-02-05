import random as rd

from gsurface.forces import SpringDampingInteraction
from gsurface.imodel import SurfaceGuidedInteractedMassSystems, SurfaceGuidedMassSystem
from gsurface.model import ForcesType, build_s0
from gsurface.surface import Surface

from .graph import StructureGraph


class SurfaceGuidedStructureSystem(SurfaceGuidedInteractedMassSystems):
    def __init__(self, surface: Surface, structure: StructureGraph, structureForces: ForcesType = None, **kargs):
        """

        :param surface: Surface on which the structure evolve
        :param structure: Structure decribed by a graph
        :param structureForces: Forces than apply on all the nodes of the structure

        to define forces than apply only on a specific node use:
         * structure_model.models[i].forces.append(Force)
        """
        if structureForces is None:
            structureForces = []

        models = [
            SurfaceGuidedMassSystem(
                surface=surface,
                s0=build_s0(rd.random() - 0.5, 0.0, rd.random() - 0.5, 0.0),
                solid=solid,
                forces=structureForces
            ) for solid in structure.nodes
        ]

        # build interactions
        interactions = [
            SpringDampingInteraction(
                [
                    models[ni],
                    models[nj]
                ],
                stiffness=params.stiffness,
                mu=params.mu,
                l0=params.l0
            ) for (ni, nj), params in structure.interactions.items()
        ]

        super(SurfaceGuidedStructureSystem, self).__init__(
            models=models,
            interactions=interactions,
        )