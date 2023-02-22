from agent import Agent
from numpy import random


class Contacts:
    def __init__(self, population):
        self.population = population

    def contact(self, agent):
        return list()


class RandomMixing(Contacts):
    def __init__(self, population):
        super().__init__(population)

    def contact(self, agent):
        n = self.population.size()
        i = random.randint(0, n-1)
        if i == agent.id:
            i += 1
        return [self.population[i]]


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
        self.agents = [None] * size
        for i in range(size):
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
