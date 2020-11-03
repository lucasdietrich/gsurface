from gsurface.surface import Surface
from gsurface.forces import SpringDampingInteraction, Force
from gsurface.imodel import SurfaceGuidedInteractedMassSystems, SurfaceGuidedMassSystem, build_s0
from gsurface.model import ForcesType

from .graph import StructureGraph

import random as rd

from typing import Tuple, Iterable

import numpy as np


class SurfaceGuidedStructureSystem(SurfaceGuidedInteractedMassSystems):
    def __init__(self, surface: Surface, structure: StructureGraph, structureForces: ForcesType = None):
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
                m=solid.mass,
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