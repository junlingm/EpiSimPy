import random
import numpy as np
from math import inf


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
