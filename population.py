
import random
import numpy as np


class Agent:
    def __init__(self, initial_state, number=None, neighbours=None, quarantined=False):
        if neighbours is None:
            neighbours = []
        self.state = initial_state
        self.number = number
        self.duration = None  # this is duration of the infectious stage
        self.neighbours = neighbours
        self.quarantined = quarantined

    def add_neighbour(self, nbr):
        self.neighbours.append(nbr)

    def set_neighbours(self, li):
        self.neighbours = li


class Population:
    def __init__(self, size, generator, per_capita_contact_rate, trace_rate):
        self.size = size
        self.agents = [None] * size
        for i in range(size):
            self.agents[i] = generator(i)
        self.contact_rate = per_capita_contact_rate
        self.trace_rate = trace_rate
        self.generator = generator

    def contact(self, agent):
        time = 0
        while time < agent.duration:
            time += np.random.exponential(1 / self.contact_rate)
            contact = random.sample(agent.neighbours, 1)[0]
            yield {"contact": contact, "time": time}

    def trace(self, agent):
        remaining = agent.neighbours
        while bool(remaining):
            time = np.random.exponential(1 / self.trace_rate)
            contact = remaining[0]
            remaining.pop(0)
            yield {"contact": contact, "time": time}

    def reset(self):
        for i in range(self.size):
            self.agents[i] = self.generator(i)
