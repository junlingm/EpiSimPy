import random


class Network:
    def __init__(self, size):
        self.size = size
        self.network = [[] for _ in range(size)]


class ER(Network):  # Erdos-Renyi model
    def __init__(self, size, p):
        super().__init__(size)
        for i in range(self.size):
            for j in range(i+1, self.size):
                if random.random() < p:
                    self.network[i].append(j)
                    self.network[j].append(i)


class WS(Network):  # Watts-Strogatz small world network
    def __init__(self, size, p, k):  # size << k, and 2|k
        super().__init__(size)
        to_reroute = [[] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(int(k/2)):
                nbr = (i + j + 1) % self.size
                to_reroute[i].append(nbr)
                self.network[i].append(nbr)
                self.network[nbr].append(i)
        for i in range(self.size):
            for v in to_reroute[i]:
                if random.random() < p:
                    new_connection = random.randint(0, self.size-1)
                    while new_connection == i or new_connection in self.network[i]:
                        new_connection = random.randint(0, self.size - 1)
                    self.network[i].append(new_connection)
                    self.network[new_connection].append(i)
                    self.network[i].remove(v)
                    self.network[v].remove(i)


