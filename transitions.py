from agent import *
from math import inf


class TransitionEvent(Event):
    """
    An event for a state transition. An optional callback function may be
    provided to be executed after the state has changed
    """
    def __init__(self, time, from_state, to_state, callback=None):
        """
        initialize a transition event

        :param time: the event time
        :param from_state: the state to change from
        :param to_state: the state to change to
        :param callback: a function to be called after the state change has happened
            If has the following arguments:
                time: the time that the transition happened
                simulation: the current simulation
                agent: the agent whose state has just changed
                from_state: the state that it has changed from
        """
        super().__init__(time)
        self.from_state = from_state
        self.to_state = to_state
        self.callback = callback

    def handle(self, sim):
        if self.from_state.match(self.owner):
            sim.set_state( self.time, self.owner, self.to_state)
            if self.callback is not None:
                self.callback(self.time, sim, self.owner, self.from_state)

class ContactEvent(Event):
    """
    An event for a state transition. An optional callback function may be
    provided to be executed after the state has changed
    """
    def __init__(self, time, contact, rule):
        """
        initialize a transition event

        :param time: the event time
        :param from_state: the state to change from
        :param to_state: the state to change to
        :param callback: a function to be called after the state change has happened
            If has the following arguments:
                time: the time that the transition happened
                simulation: the current simulation
                agent: the agent whose state has just changed
                from_state: the state that it has changed from
        """
        super().__init__(time)
        self.contact = contact
        self.rule = rule

    def handle(self, sim):
        if self.rule.from_state[0].match(self.owner) and self.rule.from_state[1].match(self.contact):
            if not self.rule.to_state[1].match(self.contact):
                sim.set_state(self.time, self.contact, self.rule.to_state[1])
            if not self.rule.to_state[0].match(self.owner):
                sim.set_state(self.time, self.owner, self.rule.to_state[0])
                if not self.rule.from_state[0].mathc(self.owner):
                    return
            self.rule.schedule(self.time, self.owner)


class Transition:
    def __init__(self, from_state, to_state, waiting_time, callback=None):
        if not isinstance(from_state, State) and not isinstance(from_state, States):
            self.from_state = State(from_state)
        else:
            self.from_state = from_state
        if not isinstance(to_state, State) and not isinstance(to_state, States):
            self.to_state = State(to_state)
        else:
            self.to_state = to_state
        self.waiting_time = waiting_time
        self.callback = callback

    def schedule(self, current_time, agent):
        if isinstance(self.from_state, State):
            if self.from_state.match(agent):
                time = self.waiting_time(current_time) + current_time
                agent.schedule(TransitionEvent(time, self.from_state, self.to_state, self.callback))
        elif self.from_state[0].match(agent):
            contacts = agent.owner.contacts(agent)
            t = inf
            contact = None
            for c, f in contacts:
                time = f(current_time)
                if time < t:
                    t = time
                    contact = c
            if t is not inf:
                agent.schedule(ContactEvent(t + current_time, contact, self))


