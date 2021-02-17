from __future__ import annotations

from typing import Iterable, List, Dict, Tuple, Union

import numpy as np

from gsurface.advanced.ode.system import ODESystem
from gsurface.forces.interaction import Interaction
from gsurface.model import SurfaceGuidedMassSystem
from gsurface.serialize.interface import SerializableInterface
from gsurface.types import ModelEvalState

InteractionMesh = Dict[Tuple[int, int], Interaction]

# for the moment we allow only one interaction between nodes and direction is determinant


class SurfaceGuidedInteractedMassSystems(ODESystem, SerializableInterface):
    def __init__(self, models: Iterable[SurfaceGuidedMassSystem], interactions: InteractionMesh = None, **kargs):
        if interactions is None:
            print("Warning : no interactions in this model")
            interactions = {}

        # todo change "model" key to "index" key (convention and serialize feature needs)

        self.models = list(models)
        self.degree = len(self.models)

        # for each interaction check if all models are well defined
        for (ni, nj), interaction in interactions.items():
            if not (0 <= ni < self.degree) or not (0 <= nj < self.degree):
                raise Exception(f"Interaction {interaction} associate object(s) that doesn't (/don't) exist : {ni} > {nj}")
            elif ni == nj:
                raise Exception(f"Interaction associating 2 times the same model is not permitted : {interaction} : {ni} > {ni}")

        self.interactions: InteractionMesh = interactions

        # build tmp ModelEvalState
        self._models_states: List[ModelEvalState] = [ModelEvalState() for model in self.models]

        # build s0
        s0 = np.concatenate([model.s0 for model in self.models])

        super(SurfaceGuidedInteractedMassSystems, self).__init__(s0)

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        ds = np.zeros_like(s)

        # eval model surface metric
        for j, (model, M) in enumerate(zip(self.models, self._models_states)):
            ms = s[4*j:4*j + 4]

            M.w = ms[::2]
            M.dw = ms[1::2]

            # todo simplify/optimize eval
            M.S, M.J, M.H = model.surface.eval(*M.w)

            M.V = M.J @ M.dw.T

            M.iF = np.zeros((3,))

        # eval interacted forces
        for (ni, nj), interaction in self.interactions.items():
            M1, M2 = self._models_states[ni], self._models_states[nj]

            F1, F2 = interaction.eval(M1, M2)

            M1.iF += F1
            M2.iF += F2

        # eval forces and build ds
        for j, (model, M) in enumerate(zip(self.models, self._models_states)):
            # eval force:
            F = model.forces.eval(t, M.S, M.V)

            # eval ds
            ds[4*j:4*j + 4] = model.ds(M.dw, F + M.iF, M.J, M.H)

        return ds

    def solutions(self, states: np.ndarray, time: np.ndarray):
        for j, model in enumerate(self.models):
            state = states[:, 4*j:4*j + 4]

            yield model.solutions(state, time)

    def __repr__(self):
        return f"{self.__class__.__name__} with {self.degree} models :\n\t" + "\n\t".join([
            str(model) for model in self.models
        ])

    # manage dict[Tuple, Class] to list[(Tuple, Class)]
    def todict(self) -> dict:
        d = super(SurfaceGuidedInteractedMassSystems, self).todict().copy()

        del d["_models_states"]

        d.update(({
            "interactions": list(self.interactions.items())
        }))

        return d

    # manage list[(Tuple, Class)] to dict[Tuple, Class]
    @classmethod
    def fromdict(cls, d: dict):
        # rebuild from StructureGraph and not subclasses
        return SurfaceGuidedInteractedMassSystems(
            models=d["models"],
            interactions={
                (na, nb): interaction for (na, nb), interaction in d["interactions"]
            }
        )

    # operators
    def __radd__(self, other: Union[SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems]) -> SurfaceGuidedInteractedMassSystems:
        if isinstance(other, SurfaceGuidedMassSystem):
            print("WARNING : The order of the models added is not respected")
        return self + other

    def __add__(self, other: Union[SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems]) -> SurfaceGuidedInteractedMassSystems:
        if isinstance(other, SurfaceGuidedInteractedMassSystems):
            interactions = self.interactions.copy()
            shift = self.degree
            interactions.update({
                (ni + shift, nj + shift): interaction for (ni, nj), interaction in other.interactions.items()
            })
            return SurfaceGuidedInteractedMassSystems(
                models=self.models + other.models,
                interactions=interactions,
            )
        elif isinstance(other, SurfaceGuidedMassSystem):
            return SurfaceGuidedInteractedMassSystems(
                models=self.models + [other],
                interactions=self.interactions
            )
        else:
            raise Exception("Can only add SurfaceGuidedMassSystem and SurfaceGuidedInteractedMassSystems models")
