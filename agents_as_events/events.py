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


class ContactEvent:
    def __init__(self):
        pass


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