from agent import *
from math import inf


class TransitionEvent(Event):
    """
    An event for a state transition. An optional callback function may be
    provided to be executed after the state has changed
    """
    def __init__(self, time, rule):
        """
        initialize a transition event

        :param time: the event time
        :param rule: the state change rule
        """
        super().__init__(time)
        self.rule = rule

    def handle(self, sim):
        if self.rule.from_state.match(self.owner):
            if self.rule.to_change is not None:
                yes = self.rule.to_change(self.time, sim, self.owner, self.rule.to_state)
                if not yes:
                    return
            sim.set_state( self.time, self.owner, self.rule.to_state)
            if self.rule.changed is not None:
                self.rule.changed(self.time, sim, self.owner, self.rule.from_state)

class ContactEvent(Event):
    """
    An event for a state transition. An optional callback function may be
    provided to be executed after the state has changed
    """
    def __init__(self, time, contact, rule):
        """
        initialize a transition event

        :param time: the event time
        :param contact: the agent to contact
        :param rule: the contact rule
        """
        super().__init__(time)
        self.contact = contact
        self.rule = rule

    def handle(self, sim):
        if self.rule.from_state[0].match(self.owner) and self.rule.from_state[1].match(self.contact):
            yes = self.rule.to_change(self.time, sim, (self.owner, self.contact), self.rule.to_state)
            if self.rule.to_change is not None and yes:
                if not self.rule.to_state[1].match(self.contact):
                    sim.set_state(self.time, self.contact, self.rule.to_state[1])
                if not self.rule.to_state[0].match(self.owner):
                    sim.set_state(self.time, self.owner, self.rule.to_state[0])
                if self.rule.changed is not None:
                    self.rule.changed(self.time, sim, (self.owner, self.contact), self.rule.from_state)
        self.rule.schedule(self.time, self.owner)


class Transition:
    def __init__(self, from_state, to_state, waiting_time=None, to_change_callback=None, changed_callback=None):
        """

        :param from_state:
        :param to_state:
        :param waiting_time:
        :param to_change_callback: a function to be called before the stqte change happens. It returns
            a boolean value. If True, the change will happen; if False, the change will not happen.
            It has the following arguments:
                time: the time that the transition happened
                simulation: the current simulation
                agent: an Agent for the state change of an agent, or a tuple of agents for the state changes
                    caused by a contact (the first initiates the contact, the second is its contact).
                to_state: the state(s) that the agent(s) will change to
        :param changed_callback: a function to be called after the state change has happened. It returns
            no value, and has the following arguments:
                time: the time that the transition happened
                simulation: the current simulation
                agent: an Agent whose state has changes, or a tuple of agents whose state has changed due
                    to contact.
                from_state: the state(s) that the agent(s) changed from
        """
        if not isinstance(from_state, State) and not isinstance(from_state, States):
            self.from_state = State(from_state)
        else:
            self.from_state = from_state
        if not isinstance(to_state, State) and not isinstance(to_state, States):
            self.to_state = State(to_state)
        else:
            self.to_state = to_state
        self.waiting_time = waiting_time
        self.to_change = to_change_callback
        self.changed = changed_callback

    def schedule(self, current_time, agent):
        if isinstance(self.from_state, State):
            if self.from_state.match(agent):
                time = self.waiting_time(current_time) + current_time
                agent.schedule(TransitionEvent(time, self))
        elif self.from_state[0].match(agent):
            contacts = agent.owner.contacts(agent)
            time = inf
            contact = None
            for c, f in contacts:
                t = f(current_time)
                if t < time:
                    time = t
                    contact = c
            if time is not inf:
                agent.schedule(ContactEvent(time + current_time, contact, self))


