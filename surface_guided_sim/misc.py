from typing import Iterable

class AverageMinMax:
    def __init__(self, data: Iterable = None):
        self.clear()

        if data is not None:
            for k in data:
                self.add(k)

    def add(self, k):
        self.sum += k
        self.min = min(k, self.min)
        self.max = max(k, self.max)
        self.n += 1

    @property
    def avg(self):
        return self.sum / self.n

    def clear(self):
        self.sum = 0.0
        self.min = float("inf")
        self.max = -float("inf")
        self.n = 0

    def __repr__(self):
        return "AverageMinMax [{n}]\navg : {avg}\nmin: {min}\nmax: {max}".format(avg=self.avg, **self.__dict__)
