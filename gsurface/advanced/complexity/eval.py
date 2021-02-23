from typing import Union

from gsurface import SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems
from .mcr import ModelComplexityRepresentation

ModelType = Union[SurfaceGuidedMassSystem, SurfaceGuidedInteractedMassSystems]


def eval_mcr(model: ModelType) -> ModelComplexityRepresentation:
    if isinstance(model, SurfaceGuidedMassSystem):
        m, f, i = model.dimension()

        return ModelComplexityRepresentation(
            imodel=0,
            model=1,
            surface=1,
            translation=model.surface.transformation.TRANSLATION,
            rotation=model.surface.transformation.ROTATION,
            force=f,
            interaction=0,
            time=0
        )
    elif isinstance(model, SurfaceGuidedInteractedMassSystems):
        m, f, i = model.dimension()

        return ModelComplexityRepresentation(
            imodel=m,
            surface=m,  # TODO : detect surface duplicate
            translation=sum(m.surface.transformation.TRANSLATION for m in model.models),
            rotation=sum(m.surface.transformation.ROTATION for m in model.models),
            force=f,
            interaction=i,
            time=0
        )
