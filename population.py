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
        self.last_contacts = []  # for the purpose of contact tracing;

    def add_neighbour(self, nbr):
        self.neighbours.append(nbr)

    def set_neighbours(self, li):
        self.neighbours = li


class Population:
    def __init__(self, size, generator, network, contact_rate, trace_rate):
        self.size = size
        self.agents = [None] * size
        self.network = network  # a list, not a class; eg. [[1,2],[0,2],[1,3],...]
        for i in range(size):
            self.agents[i] = generator(i)
            self.agents[i].set_neighbours(self.network[i])
        self.contact_rate = contact_rate
        self.trace_rate = trace_rate
        self.generator = generator

    def contact(self, agent):
        time = 0
        while bool(agent.neighbours):
            time += np.random.exponential(1 / (self.contact_rate * len(agent.neighbours)))
            contact = random.sample(agent.neighbours, 1)[0]
            yield {"contact": contact, "time": time}

    def trace(self, agent):
        for person in agent.last_contacts:
            time = np.random.exponential(1 / self.trace_rate)
            yield {"contact": person, "time": time}

    def reset(self):
        for i in range(self.size):
            self.agents[i] = self.generator(i)
            self.agents[i].set_neighbours(self.network[i])
    # this reuses the same network instead of generating a new one
