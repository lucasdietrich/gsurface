from dataclasses import dataclass

from gsurface.serialize.interface import SerializableInterface

@dataclass
class SolidParameters(SerializableInterface):
    mass: float = 1.0  # kg

    charge: float = 0.0  # C
