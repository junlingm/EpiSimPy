from events import Event
from population import Population
from loggers import *
from transitions import Transition


class Initializer:
    def initial(self, time, agent):
        return None


class InitFunction(Initializer):
    def __init__(self, func):
        self.func = func

    def initial(self, time, agent):
        return self.func(time, agent)


class Simulation(Population):
    def __init__(self, name, size, generator=None):
        super().__init__(name, size, generator)
        self.loggers = list()
        self._transitions = list()
        self.initializers = list()

    def set(self, rule):
        if isinstance(rule, Logger):
            self.loggers.append(rule)
            return

        if isinstance(rule, Transition):
            self._transitions.append(rule)
            return

        if isinstance(rule, Initializer):
            self.initializers.append(rule)

        super().set(rule)

    def run(self, times):
        values = {"times": [t for t in times]}
        n = len(times)
        for logger in self.loggers:
            if isinstance(logger, Counter):
                values[logger.name] = [0] * n

        t = times[0]
        for agent in self:
            for i in self.initializers:
                v = i.initial(t, agent)
                if isinstance(v, State):
                    self.set_state(t, agent, v)
                elif isinstance(v, Event):
                    agent.schedule(v)

        for i in range(n):
            log_time = times[i]
            while True:
                if self.time > log_time:
                    # log ...
                    for logger in self.loggers:
                        if isinstance(logger, Counter):
                            values[logger.name][i] = logger.count
                    break
                self.handle(self)
        return values

    def set_state(self, current_time, agent, state):
        for logger in self.loggers:
            logger.log(current_time, agent, state)
        agent.state.set(state)
        for rule in self._transitions:
            if rule.from_state.match(agent):
                rule.schedule(current_time, agent)
