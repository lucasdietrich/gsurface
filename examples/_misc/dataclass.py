from dataclasses import dataclass


@dataclass
class Numbers:
    a: int = 1
    b: int = 3

X = Numbers()
Y = Numbers()
Z = X

print(X, Z)

Z.a += 213

print(X, Z)