<<<<<<< HEAD
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
=======
from agent import Agent
from numpy import random


class Contacts:
    def __init__(self, population):
        self.population = population
>>>>>>> state-groups

    def contacts(self, agent):
        return list()


class RandomMixing(Contacts):
    def __init__(self, population, per_capita_rate):
        super().__init__(population)
        self.rng = lambda current_time: random.exponential(1/per_capita_rate)

<<<<<<< HEAD
class Population_network:
    def __init__(self, size, generator, network, contact_rate, trace_rate, trace_prob):
        self.size = size
=======
    def contact(self, agent):
        n = self.population.size()
        i = random.randint(0, n-1)
        if i == agent.id:
            i += 1
        return self.population[i], self.rng


class AgentIterator:
    def __init__(self, i):
        self.iterators = [i]

    def __next__(self):
        while len(self.iterators) > 0:
            try:
                p = next(self.iterators[-1])
                i = p.__iter__()
                if i is None:
                    return p
                self.iterators.append(i)
                continue
            except StopIteration:
                self.iterators.pop()
        raise StopIteration

class Population(Agent):
    """
    This class defines a population, i.e., a collection of agents.
    """

    def __init__(self, id, size, generator=None):
        """
        Initialize a population with an id, a given size, using an agent generator to generate agents

        :param id: a unique id in the simulation to represent the population
        :param size: the population size
        :param generator: a generator function for agents. Each call of this function should return a new
        agent. This function takes an integer as a single argument representing the index of the agent
        """
        super().__init__(id)
        self.contact_rules = list()
        self.generator = generator if generator is not None else lambda x: Agent(x)
>>>>>>> state-groups
        self.agents = [None] * size
        for i in range(size):
<<<<<<< HEAD
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
=======
            agent = self.generator(i)
            self.agents[i] = agent
            self.schedule(agent)

    def set(self, rule):
        if isinstance(rule, Contacts):
            self.contact_rules.append(rule)

    def __getitem__(self, item):
        """
        implements the [] operator to select an agent by index

        :param item: the index of the agent of interest
        :return: the agent at the index :param item:
        """
        return self.agents[item]

    def size(self):
        return len(self.agents)

    def __iter__(self):
        return AgentIterator(iter(self.agents))

    def contacts(self, agent):
        return [x.contact(agent) for x in self.contact_rules]
>>>>>>> state-groups
