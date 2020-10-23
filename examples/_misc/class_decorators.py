from dataclasses import dataclass


# https://stackoverflow.com/questions/59661042/what-do-single-star-and-slash-do-as-independent-parameters
def d(cls=None, /, *, y=2):
    print(cls, y)


def decorator(cls=None, *args, **kargs):
    print(cls, kargs)
    return cls


@decorator
class Hello:
    def __init__(self, name="Lucas"):
        self.name: str = name

    def cut(self):
        self.name = self.name[:3]

    def __repr__(self):
        return f"Hello {self.name} !"


x = Hello("Lucas")
