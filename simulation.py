from binarySearchTree import *
from transitions import *
from loggers import *
from events import *
from math import inf


class Simulation:
    def __init__(self, states, traced_states, population, quar_period):
        self.states = states
        self.traced_states = traced_states
        self.population = population
        self.infection_trans = {}
        self.contact_states = {}
        self.contact_trans = {}
        self.quar_period = quar_period
        self.loggers = []

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
                self.contact_trans[obj.from_state, obj.contact, obj.contact_quar] = obj
                # this assumes only one contact event between two specific states

            elif isinstance(obj, InfTrans):
                self.infection_trans[obj.from_state] += [obj]

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
                    e = next(con)
                    if e["time"] > agent.duration:
                        break
                    self.events.insert(ContactEvent(self.population.agents[e['contact']],
                                                    contacter=agent), e['time'] + self.time)

            if agent.state in self.traced_states:  # if the person joined a traced state
                trc = self.population.trace(agent, self.time, self.quar_period)
                while True:
                    try:
                        e = next(trc)
                        self.events.insert(TraceEvent(self.population.agents[e["contact"]], agent),
                                           e["time"] + self.time)
                    except StopIteration:
                        break

        for person in self.population.agents:
            new_events(person)

        while bool(times) and self.events.root is not None:

            next_event = self.events.remove_smallest()

            while bool(times) and next_event.value > times[0]:
                for logger in self.loggers:
                    data[logger.name].append(logger.value)
                data["time"].append(times[0])
                times.pop(0)

            if isinstance(next_event.event, SelfEvent):

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

                elif isinstance(transition, QuarTrans):

                    person.quarantined = False
                    self.time = next_event.value

                    for logger in self.loggers:
                        logger.log(person.state, person.state, True, False)

            elif isinstance(next_event.event, ContactEvent):
                person = next_event.event.person
                contacter = next_event.event.contacter
                if (person.state, contacter.state, contacter.quarantined) in self.contact_trans:
                    transition = self.contact_trans[person.state, contacter.state, contacter.quarantined]
                    contacter.last_contacts[person.number] = next_event.value
                    if transition.valid():

                        # this comes before the state is changed
                        for logger in self.loggers:
                            logger.log(person.state, transition.to_state, person.quarantined, person.quarantined)

                        person.state = transition.to_state
                        self.time = next_event.value  # this needs to come before new_events()

                        new_events(person)

            elif isinstance(next_event.event, TraceEvent):
                person = next_event.event.person
                # contact = next_event.event.contact # this variable isn't necessary in the current implementation
                if person.state not in self.traced_states:
                    if not person.quarantined:

                        person.quarantined = True

                        for logger in self.loggers:
                            logger.log(person.state, person.state, False, True)

                        person.last_quar = next_event.value  # updates the latest reason for being quarantined
                        self.time = next_event.value
                        self.events.insert(SelfEvent(person, QuarTrans(None, True, False)),
                                           self.time + self.quar_period)
        return data

    def reset(self):
        pass  # currently this is implemented at the top of the run() method
