import typing
from collections import defaultdict, OrderedDict
from typing import Iterable, List, Dict, Tuple

import numpy as np
from ode.system import ODESystem

from gsurface.types import ModelEvalState
from gsurface.forces.interaction import Interaction
from gsurface.model import SurfaceGuidedMassSystem, build_s0

ModelsEvalStates = typing.OrderedDict[SurfaceGuidedMassSystem, ModelEvalState]


class SurfaceGuidedInteractedMassSystems(ODESystem):
    def __init__(self, models: List[SurfaceGuidedMassSystem], interactions: Iterable[Interaction] = None):
        if interactions is None:
            print("Warning : no interactions in this model")
            interactions = []

        # todo change "model" key to "index" key
        self.models: ModelsEvalStates = OrderedDict({model: ModelEvalState() for model in models})

        self.degree = len(models)

        # build s0
        s0 = np.concatenate([model.s0 for model in self.models])

        # for each interaction check if all models are well defined
        self.interactions: List[Interaction] = []
        for interaction in interactions:
            for model in interaction.models:
                if model not in self.models:
                    raise Exception("A model defined in an interaction is not defined in the list of simulation models")
            self.interactions.append(interaction)

        super(SurfaceGuidedInteractedMassSystems, self).__init__(s0)

    def _derivs(self, s: np.ndarray, t: float) -> np.ndarray:
        ds = np.zeros_like(s)

        # eval model surface metric
        for j, (model, M) in enumerate(self.models.items()):
            ms = s[4*j:4*j + 4]

            M.w = ms[::2]
            M.dw = ms[1::2]

            # todo simplify/optimize eval
            M.S, M.J, M.H = model.surface.eval(*M.w)

            M.iF = np.zeros((3,))

        # eval interacted forces
        for interaction in self.interactions:
            m1, m2 = interaction.models
            M1, M2 = self.models[m1], self.models[m2]
            F1, F2 = interaction.eval(M1, M2)

            M1.iF += F1
            M2.iF += F2

        # eval forces and build ds
        for j, (model, M) in enumerate(self.models.items()):
            # eval force:
            F = model.forces.eval(M.w, M.dw, t, M.S, M.J)

            # eval ds
            ds[4*j:4*j + 4] = model.ds(M.dw, F + M.iF, M.J, M.H)

        return ds

    def solutions(self, states: np.ndarray, time: np.ndarray):
        for j, model in enumerate(self.models):
            state = states[:, 4*j:4*j + 4]

            yield model.solutions(state, time)
