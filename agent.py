from math import inf
from events import Event
from sortedcontainers import SortedList


class State:
    """
    Abstracts a specific state
    """
    def __init__(self, value=None, key=None):
        if key is None:
            self.value = value
        else:
            self.value = {key: value}

    def set(self, value):
        if isinstance(value, State):
            value = value.value
        if not isinstance(value, dict):
            self.value = value
        elif not isinstance(value, dict):
            raise ValueError
        else:
            for k in value:
                self.value[k] = value[k]

    def __setitem__(self, key, value):
        if (key is None) or (key == "value"):
            self.value = value
        elif self.value is None:
            self.value = {key: value}
        elif isinstance(self.value, dict):
            self.value[key] = value
        else:
            raise KeyError

    def __getitem__(self, item=None):
        return self.value if item is None else self.value[item]

    def __and__(self, other):
        if not isinstance(other, State):
            return self & State(other)
        state = self
        if not isinstance(self.value, dict):
            return state if self.value == other.value else State()

        if not isinstance(other.value, dict):
            return State()

        for key in other.value:
            if key not in state.value:
                state.value[key] = other.value[key]
            elif state.value[key] != other.value[key]:
                return State()
        return state

    def __repr__(self):
        return str(self.value)

    def match(self, other):
        """
        check if this state matches the other state. A state matches the other if
        it is a subset of the other state.

        :param other: the state or an agent to match
        :return: a boolean value
        """
        if isinstance(other, Agent):
            return self.match(other.state)
        if not isinstance(other, State):
            return self.match(State(other))
        if not isinstance(self.value, dict):
            return self.value == other.value
        if not isinstance(other.value, dict):
            return False

        for key in self.value:
            if key not in other.value:
                return False
            if other.value[key] != self.value[key]:
                return False
        return True

    def __add__(self, other):
        if isinstance(other, State):
            return States(self, other)
        if isinstance(other, States):
            return States(self)+other
        raise ValueError


class States:
    """
    This class abstracts the states of multiple agents
    """
    def __init__(self, *states):
        """
        initialize with a given tuple of states
        :param states: a tuple of object, each can be of class State, States
        """
        self.states = ()
        for state in states:
            self.__add__(state)

    def __repr__(self):
        return str(self.states)

    def __add__(self, other):
        if isinstance(other, State):
            self.states += (other,)
        elif isinstance(other, States):
            self.states += other.states
        else:
            raise ValueError

    def match(self, agent):
        return self.states[0].match(agent)

    def __getitem__(self, item):
        return self.states[item]



class Agent(Event):
    """
    An abstraction of an agent. Each agent has a list of events attached to it. They themselves are events,
    with the event time being the time of its first event. Thus, an agent can be scheduled in a population.

    Methods:
        handle: handle the first event
        schedule: schedule an event
        unschedule: unschedule an event
    """
    def __init__(self, id):
        """
        initialize an agent with a given id, and set up an empty event list
        :param id: the id of the agent
        """
        # Each agent maintains a list of events, organized by as a binary search tree
        self.events = SortedList()
        # an empty list of event corresponds to an event time at infinity
        super().__init__(inf)
        # initial state
        self.id = id
        self.state = State()

    def handle(self, sim):
        if len(self.events) == 0:
            return
        self.events.pop(0).handle(sim)
        if len(self.events) == 0:
            self.time = inf
        else:
            self.time = self.events[0].time
        if self.owner is not None:
            self.owner.schedule(self)

    def schedule(self, event):
        """
        Schedule an event

        :param event: the event to schedule
        """
        if (event.owner is not None) and (event.owner != self):
            raise ValueError

        event.owner = self
        if event.time is inf:
            return

        self.events.add(event)

        # check if the earliest event time has changed
        if event.time < self.time:
            owner = self.owner
            if owner is not None:
                owner.unschedule(self)
            self.time = event.time
            if owner is not None:
                owner.schedule(self)

    def unschedule(self, event):
        """
        unschedule a given event

        :param event: the event to unschedule, must be an Event object
        """
        if event.owner != self:
            raise ValueError

        if event.time == inf:
            return

        # find event, store its index in i
        i = self.events.index(event)
        while self.events[i] is not event:
            if self.events[i] > event:
                raise ValueError
            i = i + 1
        # remove the event
        self.events.pop(i)
        event.owner = None
        # check if the earliest event has changed
        if len(self.events) == 0:
            time = inf
        else:
            time = self.events[0].time
        if self.time != time:
            if self.owner is not None:
                self.owner.unschedule(self)
            self.time = time
            if self.owner is not None:
                self.owner.schedule(self)

    def __iter__(self):
        return None