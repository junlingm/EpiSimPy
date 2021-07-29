from math import inf
from functools import total_ordering
from sortedcontainers import SortedList


@total_ordering
class Event:
    def __init__(self, time):
        # time: event time
        self.time = time
        # owner: the agent that owns the event
        self.owner = None

    def handle(self, owner):
        pass

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time


class ContactEvent(Event):
    def __init__(self, time, contact):
        super().__init__(time)
        self.contact = contact

    def handle(self, owner):
        pass


class InfEvent(Event):
    def __init__(self, time, from_state, to_state):
        super().__init__(time)
        self.from_state = from_state
        self.to_state = to_state


class I_R(InfEvent):
    def __init__(self, time):
        super().__init__(time, "I", "R")

    def handle(self, owner):
        if owner.state == self.from_state:
            owner.state = self.to_state


class Agent(Event):
    def __init__(self, number, neighbours):
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
