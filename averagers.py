class Averager(list):
    def __init__(self):
        self.n = 0

    def __iadd__(self, other):  # assume all data has same times and size
        if len(self) == 0:
            for v in other:
                self.append(v)
        else:
            for i in range(len(self)):
                self[i] = (self[i] * self.n + other[i]) / (self.n + 1)
        self.n += 1
        return self
