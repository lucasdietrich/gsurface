from __future__ import annotations

import math
import re
from dataclasses import dataclass


@dataclass
class ModelComplexityRepresentation:
    _mcr_rec = re.compile(r"^((iM(?P<imodel>\d+))|(?P<model>M))"
                         r"(-(S(?P<surface>\d*))(T(?P<translation>\d*))?(R(?P<rotation>\d*))?)?"
                         r"(-(F(?P<force>\d*))?(I(?P<interaction>\d*))?)?"
                         r"-(T(?P<time>\d+))$")

    imodel: int
    model: int
    surface: int
    translation: int
    rotation: int
    force: int
    interaction: int
    time: int

    def __post_init__(self):
        if self.model:
            self.model = 1
        else:
            self.model = self.imodel = int(self.imodel)

        self.surface = int(self.surface) if self.surface else 1
        self.translation = int(self.translation) if self.translation else 0
        self.rotation = int(self.rotation) if self.rotation else 0
        self.force = int(self.force) if self.force else 0
        self.interaction = int(self.interaction) if self.interaction else 0
        self.time = int(self.time) if self.time else 0

    def complexity(self) -> int:
        return self.model * self.surface * (1 + self.translation + self.rotation) * (1 + self.force + self.interaction) * self.time

    def mcr_number(self) -> int:
        return int(math.log2(self.complexity()))

    @staticmethod
    def from_mcr(mcr: str) -> ModelComplexityRepresentation:
        m = ModelComplexityRepresentation._mcr_rec.match(mcr)

        if m:
            return ModelComplexityRepresentation(**m.groupdict())

    def mcr(self, exhaustive: bool = False) -> str:
        return "-".join(_ for _ in
            [
                self._format_group_model(),
                self._format_group_surface(exhaustive),
                self._format_group_force(exhaustive),
                self._format_group_time()
            ] if _ != ""
        )

    @staticmethod
    def _format_component(letter: str, component: int, exhaustive: bool = False) -> str:
        f = ""

        if component is None:
            component = 0

        if component != 0 or exhaustive:
            f += letter

            if component != 1 or exhaustive:
                f += f"{component}"

        return f

    def _format_group_model(self) -> str:
        if self.imodel:
            return self._format_component("iM", self.imodel, True)
        else:
            return "M"

    def _format_group_surface(self, exhaustive: bool = False) -> str:
        return self._format_component("S", self.surface, exhaustive) + self._format_component("T", self.translation, exhaustive) + self._format_component("R", self.rotation, exhaustive)

    def _format_group_force(self, exhaustive: bool = False) -> str:
        return self._format_component("F", self.force, exhaustive) + self._format_component("I", self.interaction, exhaustive)

    def _format_group_time(self) -> str:
        return f"T{self.time}"

    def __eq__(self, other: ModelComplexityRepresentation):
        return self.mcr() == other.mcr()

    def __repr__(self):
        return "mcr : " + self.mcr()
