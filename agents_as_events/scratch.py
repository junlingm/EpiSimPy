from math import inf
from functools import total_ordering
from sortedcontainers import SortedList


@total_ordering
class Event:
    """
    An abstraction of an event

    It contains two instance variables:
        time: the event time
        owner: the agent whom this event is attached to

    It has a n important method:
        handle: it processes this event
    """

    def __init__(self, time):
        """
        constructor.

        :param time: the time of the event
        :return: None
        """
        # instance variables:
        # time: event time
        self.time = time
        # owner: the agent that owns the event
        self.owner = None

    def handle(self, owner):
        """
        handle the event

        :param owner: the previous owner of this event. Note that when the event is handled, it has already be unscheduled
        :return: None
        """
        pass

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time


class Agent(Event):
    """
    An abstraction of an agent. Each agent has a list of events attached to it. They themselves are events, with the event
    time being the time of its first event. Thus, an agent can be scheduled in a population.

    Methods:
        handle: handle the first event
        schedule: schedule an event
        unschedule: unschedule an event
    """

    def __init__(self):
        # Each agent maintains a list of events, organized by as a binary search tree
        self.events = SortedList()
        # an empty list of event corresponds to an event time at infinity
        super().__init__(inf)

    def handle(self, owner):
        if len(self.events) == 0:
            return
        event = self.events.pop(0)
        event.owner = None
        if event is not None:
            event.handle(self)
        if len(self.events) == 0:
            self.time = inf
        else:
            self.time = self.events[0].time
        if owner is not None:
            owner.schedule(self)

    def schedule(self, event):
        """
        Schedule an event

        :param event: the event to schedule
        :return: None
        """
        if event.owner is not None:
            raise ValueError

        event.owner = self
        if event.time is inf:
            return

        self.events.add(event)

        # check if the earliest event time has changed
        if event.time < self.time:
            if self.owner is not None:
                self.owner.unschedule(self)
            self.time = event.time
            if self.owner is not None:
                self.owner.schedule(self)

    def unschedule(self, event):
        if event.owner != self:
            raise ValueError

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


class Simulation(Agent):
    def __init__(self, population):
        super().__init__()
        self.agents = population
        for agent in population:
            self.schedule(agent)

    def run(self, times):
        for log_time in times:
            while True:
                time = self.time
                if time > log_time:
                    # log ...
                    print("time:", log_time)
                    break
                self.handle(None)


class TestEvent(Event):
    """
    A test event that recurs at a given list of time. It assigns the state of the agent to its name
    """

    def __init__(self, name, times):
        self.times = times
        self.name = name
        super().__init__(self.next())

    def next(self):
        if len(self.times) == 0:
            return inf
        return self.times.pop(0)

    def __repr__(self):
        return "TestEvent(%f, %s)" % (self.time, self.name)

    def handle(self, owner):
        print(self, "handled")
        self.time = self.next()
        owner.state = self.name
        owner.schedule(self)


e1 = TestEvent("e1", [1.1, 2.1, 3.1])
e2 = TestEvent("e2", [1, 2, 3, 4])

p = Agent()
p.schedule(e1)
p.schedule(e2)

test = Simulation([p])
test.schedule(TestEvent("e3", [2.5]))
test.run(range(10))
print("agent final state:", p.state)
print("simulation final state:", test.state)
