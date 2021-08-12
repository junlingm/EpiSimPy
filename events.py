from functools import total_ordering


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

    def handle(self, sim):
        """
        handle the event

        :param sim: the current simulation
        :param owner: the previous owner of this event. Note that when the event is handled,
            it has already be unscheduled
        :return: None
        """
        pass

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time
