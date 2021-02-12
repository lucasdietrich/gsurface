import random as rd

from gsurface.forces import SpringDampingInteraction
from gsurface.imodel import SurfaceGuidedInteractedMassSystems, SurfaceGuidedMassSystem
from gsurface.model import ForcesType, build_s0
from gsurface.surface import Surface

from .graph import StructureGraph

import numpy as np


class SurfaceGuidedStructureSystem(SurfaceGuidedInteractedMassSystems):
    def __init__(self, surface: Surface, structure: StructureGraph, s0=None, structureForces: ForcesType = None,
                 **kargs):
        """
        Simulate structure composed of mass point objects evolving on a same surface

        :param surface: Surface on which the structure evolve
        :param structure: Structure decribed by a graph
        :param structureForces: Forces than apply on all the nodes of the structure

        to define forces than apply only on a specific node use:
         * structure_model.models[i].forces.append(Force)
        """
        if structureForces is None:
            structureForces = []

        if s0 is None:
            s0 = np.zeros(4*structure.N)

        # see how to serialize
        # self._surface = surface
        # self._structure = structure
        # self._structureForces = structureForces

        # build models
        models = [
            SurfaceGuidedMassSystem(
                surface=surface,
                s0=s0[4*i: 4*i+4],
                solid=solid,
                forces=structureForces
            ) for i, solid in enumerate(structure.nodes)
        ]

        # build interactions
        interactions = {
            (ni, nj): SpringDampingInteraction(
                stiffness=params.stiffness,
                mu=params.mu,
                l0=params.l0
            ) for (ni, nj), params in structure.interactions.items()
        }

        super(SurfaceGuidedStructureSystem, self).__init__(
            models=models,
            interactions=interactions,
        )
