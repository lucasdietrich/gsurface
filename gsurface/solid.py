from dataclasses import dataclass
from typing import Union

from gsurface.serialize.interface import SerializableInterface


@dataclass
class Solid(SerializableInterface):
    mass: float = 1.0  # kg (symbol m)
    charge: float = 0.0  # C (symbol q)

    # other caractéristics

    def __repr__(self):
        return f"{self.mass:.2f} kg" + (f", {self.charge:.3f} C" if self.charge else "")


SOLID = Union[float, Solid]


def toSolid(any: SOLID) -> Solid:
    if isinstance(any, Solid):
        return any
    elif isinstance(any, float):
        return Solid(mass=any)
    else:
        raise TypeError("A Solid definition is expected")
