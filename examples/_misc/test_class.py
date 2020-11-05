class SomeObject:
    def __init__(self, a: float = 0.0, b: float = 0.0, **kargs):
        self.a = a
        self.b = b

    @classmethod
    def fromdict(cls, d: dict):
        return cls(**d)


if __name__ == "__main__":
    so = SomeObject(1.0, 2.0)