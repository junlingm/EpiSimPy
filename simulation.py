from events import Event
from population import Population
from loggers import *
from transitions import Transition


<<<<<<< HEAD
class Simulation:
    def __init__(self, states, traced_states, population, quar_period, pos_test,
                 quar_test_time=None, periodic_test_interval=None):
        self.states = states
        self.traced_states = traced_states
        self.population = population
        self.infection_trans = {}
        self.contact_states = {}
        self.contact_trans = {}
        self.test_trans = {}
        self.quar_period = quar_period
        self.loggers = []
        self.pos_test = pos_test
        self.periodic_test_interval = periodic_test_interval
        self.quar_test_time = quar_test_time
=======
class Initializer:
    def initial(self, time, agent):
        return None
>>>>>>> state-groups


class InitFunction(Initializer):
    def __init__(self, func):
        self.func = func

<<<<<<< HEAD
    def define(self, obj):
        if isinstance(obj, Transition):
            if isinstance(obj, Contact):
                self.contact_states[obj.contact, obj.contact_quar] = True
                self.contact_trans[obj.from_state, obj.self_quar, obj.contact, obj.contact_quar] = obj
                # this assumes only one contact event between two specific states
=======
    def initial(self, time, agent):
        return self.func(time, agent)
>>>>>>> state-groups


<<<<<<< HEAD
            elif isinstance(obj, TestTrans):
                self.test_trans[(obj.from_state, obj.from_quar)] = obj
                # there should only be one test transition for each state

        elif isinstance(obj, Logger):
            self.loggers += [obj]

    def run(self, times):
        self.events.clear()  # reset the tree so that the simulation can be run multiple times
        data = {"time": []}
        times = list(times)
        self.time = 0
        for logger in self.loggers:
            data[logger.name] = []
            logger.reset()
        self.population.reset()  # reset population
        for time in times:
            self.events.insert(UpdateEvent(), time)
        if self.periodic_test_interval is not None:
            for pers in self.population.agents:
                t = self.population.p_test(self.periodic_test_interval)
                self.events.insert(PeriodicTestEvent(pers), t)

        def new_events(agent):
            agent.duration = None
            min_time = inf
            next_trans = None
            for trans in self.infection_trans[agent.state]:
                new_time = trans.waiting_time()
                if new_time < min_time:
                    min_time = min(min_time, new_time)
                    next_trans = trans
            if min_time < inf:
                self.events.insert(SelfEvent(agent, next_trans), min_time + self.time)
                agent.duration = min_time
            if (agent.state, agent.quarantined) in self.contact_states:
                con = self.population.contact(agent)
                while True:
                    try:
                        e = next(con)
                        if e["time"] > agent.duration:
                            break
                        self.events.insert(ContactEvent(self.population.agents[e['contact']],
                                                        contacter=agent), e['time'] + self.time)
                    except StopIteration:
                        break
            if (agent.state, agent.quarantined) in self.test_trans:

                trans = self.test_trans[(agent.state, agent.quarantined)]
                t = trans.waiting_time()
                self.events.insert(TestPosEvent(agent, trans), self.time + t)

        def new_trace_events(agent):
            if (agent.state, agent.quarantined) in self.traced_states:
                agent.traced = True
            if agent.traced and not agent.was_traced:
                # if the person joined a traced state
                # I will assume that the same person will not have their contacts traced twice
                agent.was_traced = True
                trc = self.population.trace(agent)
                while True:
                    try:
                        e = next(trc)
                        pers = self.population.agents[e["contact"]]
                        if pers.state not in self.traced_states:
                            if not pers.quarantined:

                                pers.quarantined = True

                                for logger in self.loggers:
                                    logger.log(pers.state, pers.state, False, True)

                                self.time = next_event.value
                                self.events.insert(SelfEvent(pers, QuarTrans(None, True, False)),
                                                   self.time + self.quar_period)
                                if self.quar_test_time is not None and pers.state in self.pos_test:
                                    t = self.quar_test_time()
                                    self.events.insert(TestPosEvent(pers, None), self.time + t)
                                new_trace_events(pers)
                    except StopIteration:
                        break

        for person in self.population.agents:
            new_events(person)
        while self.events.root is not None and self.time <= times[-1]:

            next_event = self.events.remove_smallest()
            #print(next_event.value)
            #print(isinstance(next_event.event, PeriodicTestEvent))
            if isinstance(next_event.event, UpdateEvent):
                for logger in self.loggers:
                    data[logger.name].append(logger.value)
                data["time"].append(next_event.value)
                if next_event.event.end_sim:
                    return data

            elif isinstance(next_event.event, SelfEvent):

                person = next_event.event.person
                transition = next_event.event.transition

                if isinstance(transition, InfTrans):
                    if person.state == transition.from_state:

                        person.state = transition.to_state
                        self.time = next_event.value  # this needs to come before new_events()

                        for logger in self.loggers:
                            logger.log(transition.from_state,
                                       transition.to_state, person.quarantined, person.quarantined)
                        new_events(person)
                        new_trace_events(person)

                elif isinstance(transition, QuarTrans):
                    # does quarantine end regardless of a new test?
                    person.quarantined = False
                    self.time = next_event.value
=======
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
>>>>>>> state-groups

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
<<<<<<< HEAD
                        logger.log(person.state, person.state, True, False)

                    new_trace_events(person)

            elif isinstance(next_event.event, TestPosEvent):
                person = next_event.event.person
                if person.state in self.pos_test:  # find a better way to implement this
                    for logger in self.loggers:
                        logger.log(person.state, person.state, person.quarantined, True)
                    person.quarantined = True
                    person.traced = True
                    new_trace_events(person)

            elif isinstance(next_event.event, ContactEvent):
                person = next_event.event.person
                contacter = next_event.event.contacter
                if (person.state, person.quarantined, contacter.state, contacter.quarantined) in self.contact_trans:
                    transition = self.contact_trans[person.state, person.quarantined, contacter.state, contacter.quarantined]
                    if person.number not in contacter.last_contacts:
                        contacter.last_contacts.append(person.number)
                    if transition.valid():
                        # no longer assumes susceptible quarantined people not infected

                        # this comes before the state is changed
                        for logger in self.loggers:
                            logger.log(person.state, transition.to_state, person.quarantined, person.quarantined)

                        person.state = transition.to_state
                        self.time = next_event.value  # this needs to come before new_events()

                        new_events(person)
                        new_trace_events(person)

            elif isinstance(next_event.event, TraceEvent):
                person = next_event.event.person
                if person.state not in self.traced_states:
                    if not person.quarantined:

                        person.quarantined = True

                        for logger in self.loggers:
                            logger.log(person.state, person.state, False, True)

                        self.time = next_event.value
                        self.events.insert(SelfEvent(person, QuarTrans(None, True, False)),
                                           self.time + self.quar_period)
                        if self.quar_test_time is not None and person.state in self.pos_test:
                            t = self.quar_test_time()
                            self.events.insert(TestPosEvent(person, None), self.time + t)
                        new_trace_events(person)

            elif isinstance(next_event.event, PeriodicTestEvent):
                pers = next_event.event.person
                self.time = next_event.value
                if pers.state in self.pos_test:
                    self.events.insert(TestPosEvent(pers, None), self.time)
                elif not pers.was_traced:
                    t = self.population.p_test(self.periodic_test_interval)
                    self.events.insert(PeriodicTestEvent(pers), self.time+t)

        return data

    def reset(self):
        pass  # currently this is implemented at the top of the run() method
=======
                        if isinstance(logger, Counter):
                            values[logger.name][i] = logger.count
                    break
                self.handle(self)
        return values

    def set_state(self, current_time, agent, state):
        from_state = State(agent.state)
        agent.state.set(state)
        for logger in self.loggers:
            logger.log(current_time, agent, from_state)
        for rule in self._transitions:
            if (not rule.from_state.match(from_state)) and rule.from_state.match(agent):
                rule.schedule(current_time, agent)
>>>>>>> state-groups
