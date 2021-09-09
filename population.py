import random
import numpy as np
from math import inf

# code for random mixing model
class Agent:
    def __init__(self, initial_state, number=None, size=None, quarantined=False, traced=False):
        self.state = initial_state
        self.number = number
        self.duration = None  # this is duration of the infectious stage
        self.size = size
        self.quarantined = quarantined
        self.traced = traced  # the person has been/ should be traced
        self.was_traced = False  # the person has been traced
        self.last_contacts = []  # for the purpose of contact tracing;


class Population:
    def __init__(self, size, generator, global_contact_rate, trace_rate, trace_prob):
        self.size = size
        self.agents = [None] * size
        for i in range(size):
            self.agents[i] = generator(i, size)
        self.contact_rate = global_contact_rate
        self.trace_rate = trace_rate
        self.generator = generator
        self.trace_prob = trace_prob

    def contact(self, agent):
        time = 0
        while True:
            time += np.random.exponential(1 / self.contact_rate)
            contact = random.randint(0, self.size - 2)
            if contact >= agent.number:
                contact += 1
            yield {"contact": contact, "time": time}

    def trace(self, agent):
        for person in agent.last_contacts:
            if random.random() < self.trace_prob:
                if self.trace_rate == inf:
                    yield {"contact": person, "time": 0}
                time = np.random.exponential(1 / self.trace_rate)
                yield {"contact": person, "time": time}

    def p_test(self, period):
        return np.random.exponential(period)

    def reset(self):
        for i in range(self.size):
            self.agents[i] = self.generator(i, self.size)


# code for network based model
class Agent_network:
    def __init__(self, initial_state, number=None, neighbours=None, quarantined=False, traced=False):
        if neighbours is None:
            neighbours = []
        self.state = initial_state
        self.number = number
        self.duration = None  # this is duration of the infectious stage
        self.neighbours = neighbours
        self.quarantined = quarantined
        self.traced = traced  # the person has been/ should be traced
        self.was_traced = False  # the person has been traced
        self.last_contacts = []  # for the purpose of contact tracing;

    def add_neighbour(self, nbr):
        self.neighbours.append(nbr)

    def set_neighbours(self, li):
        self.neighbours = li


class Population_network:
    def __init__(self, size, generator, network, contact_rate, trace_rate, trace_prob):
        self.size = size
        self.agents = [None] * size
        self.network = network  # a list, not a class; eg. [[1,2],[0,2],[1,3],...]
        for i in range(size):
            self.agents[i] = generator(i)
            self.agents[i].set_neighbours(self.network[i])
        self.contact_rate = contact_rate
        self.trace_rate = trace_rate
        self.generator = generator
        self.trace_prob = trace_prob

    def contact(self, agent):
        time = 0
        while bool(agent.neighbours):
            time += np.random.exponential(1 / (self.contact_rate * len(agent.neighbours)))
            contact = random.sample(agent.neighbours, 1)[0]
            yield {"contact": contact, "time": time}

    def trace(self, agent):
        for person in agent.last_contacts:
            if random.random() < self.trace_prob:
                if self.trace_rate == inf:
                    yield {"contact": person, "time": 0}
                time = np.random.exponential(1 / self.trace_rate)
                yield {"contact": person, "time": time}

    def p_test(self, period):
        return np.random.exponential(period)

    def reset(self):
        for i in range(self.size):
            self.agents[i] = self.generator(i)
            self.agents[i].set_neighbours(self.network[i])
    # this reuses the same network instead of generating a new one