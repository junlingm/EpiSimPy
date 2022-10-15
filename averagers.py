import numpy as np

class Averager(list):
    def __init__(self):
        self.n = 0

    def __iadd__(self, other):  # assume all data has same times and size
        self.append(other)
        n = len(other)
        if self.n < n:
            self.n = n
        return self

    def mean(self):
        if self.n == 0:
            return []
        v = [0] * self.n
        for a in self:
            for i in range(self.n):
                v[i] += a[i] if i < len(a) else 0
        n = len(self)
        for i in range(self.n):
            v[i] /= n
        return v

    def std(self):
        if self.n == 0:
            return []
        m = self.mean()
        v = [0] * self.n
        for a in self:
            for i in range(self.n):
                x = a[i] if i < len(a) else 0
                v[i] += (x - m[i]) ** 2
        n = len(self)
        for i in range(self.n):
            v[i] = np.sqrt(v[i]/n)
        return v

    def quantile(self, q):
        if self.n == 0:
            return []
        v = [0] * self.n
        n = len(self)
        m = np.zeros((self.n, n))
        for i in range(n):
            a = self[i]
            m[0:len(a), i] = a
        for i in range(self.n):
            v[i] = np.quantile(m[i, ], q)
        return v
