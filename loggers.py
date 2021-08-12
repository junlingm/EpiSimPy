from agent import State


class Logger:
    """
    This class logs state changes
    """
    def __init__(self, from_state, to_state=None):
        """
        set up a logger that matches the state change from from_state to to_state. If to_state is
        None, then it logs the stte changes enteriong and leaving the from_state.

        :param from_state: the state that will be changed.
        :param to_state: the state that will be changed to. None matches anything
        """
        if isinstance(from_state, State):
            self.from_state = from_state
        else:
            self.from_state = State(from_state)
        if isinstance(to_state, State) or to_state is None:
            self.to_state = to_state
        else:
            self.to_state = State(to_state)

    def log(self, time, agent, to_state):
        """
        the agent's state has changed from from_state to to_state. Log this event if it matches.
        :param time: the time that the state changed
        :param agent: the agent
        :param to_state: the agent's next state
        """
        pass

class Counter(Logger):
    """
    A logger that counts the number of matched state changes
    """
    def __init__(self, name, state, to_state=None, initial=0):
        """
        set up a counter that matches the state changes.

        :param name: the name of the logger
        :param state: If to_state is None this counter logs the number of agents currently in this state.
            Otherwise, this counter longs the number of transitions that leaves this state, and entering
            the to_state
        :param to_state: the state that will be changed to.
        :param initial: the initial value
        """
        super().__init__(state, to_state)
        self.name = name
        self.count = initial

    def log(self, time, agent, to_state):
        if self.to_state is None:
            if self.from_state.match(agent):
                self.count -= 1
            elif self.from_state.match(to_state):
                self.count += 1
        elif self.from_state.match(agent) and self.to_state.match(to_state):
            self.count += 1
