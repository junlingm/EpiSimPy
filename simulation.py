from binarySearchTree import *
from transitions import *
from loggers import *
from events import *
from math import inf


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

        for state in self.states:
            self.infection_trans[state] = []

        # current time
        self.time = None
        # the events organized in the binary search tree
        self.events = BinarySearchTree()

    def define(self, obj):
        if isinstance(obj, Transition):
            if isinstance(obj, Contact):
                self.contact_states[obj.contact, obj.contact_quar] = True
                self.contact_trans[obj.from_state, obj.self_quar, obj.contact, obj.contact_quar] = obj
                # this assumes only one contact event between two specific states

            elif isinstance(obj, InfTrans):
                self.infection_trans[obj.from_state] += [obj]

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
            for i in range((times[-1]//self.periodic_test_interval)+1):
                self.events.insert(PeriodicTestEvent(), i*self.periodic_test_interval)

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
                        self.events.insert(TraceEvent(self.population.agents[e["contact"]], agent),
                                           e["time"] + self.time)
                    except StopIteration:
                        break

        for person in self.population.agents:
            new_events(person)
        while self.events.root is not None and self.time <= times[-1]:

            next_event = self.events.remove_smallest()

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

                    for logger in self.loggers:
                        logger.log(person.state, person.state, True, False)

                    new_trace_events(person)

            elif isinstance(next_event.event, TestPosEvent):
                person = next_event.event.person
                if person.state != "R":  # find a better way to implement this
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
                for person in self.population.agents:
                    if person.state in self.pos_test:
                        self.events.insert(TestPosEvent(person, None), next_event.value)

        return data

    def reset(self):
        pass  # currently this is implemented at the top of the run() method
