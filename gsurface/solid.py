from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class SolidParameters:
    mass: float = 1.0  # kg

    charge: float = 0.0  # C
