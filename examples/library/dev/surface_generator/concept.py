from typing import Tuple, Callable

# form y(x) > y : x > (x, y)
def y(x: float) -> float:
    return x**2

def to_parametric(f: Callable[[float], float]):
    def yp(p: float) -> Tuple[float, float]:
        return (p, f(p))
    return yp

# form parametric(p) > (x, y) : p > (x, y)
def parametric(p: float) -> Tuple[float, float]:
    return (p, p**2)
