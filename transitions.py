import numpy as np


class Transition:
    def __init__(self, from_state, to_state, waiting_time):
        self.from_state = from_state
        self.to_state = to_state
        self.waiting_time = waiting_time
        self.contact = None


class InfTrans(Transition):
    def __init__(self, from_state, to_state, waiting_time):
        super().__init__(from_state, to_state, waiting_time)


class Contact(Transition):
    def __init__(self, from_state, to_state, contact_state, contact_quar, chance):
        super().__init__(from_state, to_state, None)
        # this has to come after
        self.contact = contact_state
        self.contact_quar = contact_quar

        # this is the chance that the contact produces a valid event, eg. if infectivity is reduced for the E class
        self.chance = chance

    def valid(self):
        return np.random.binomial(1, self.chance) == 1
    # 1 is true, 0 is false


class QuarTrans(Transition):
    def __init__(self, from_state, from_quar, to_quar):
        super().__init__(from_state, from_state, None)
        self.from_quar = from_quar
        self.to_quar = to_quar


class TestTrans(Transition):
    # it is assumed that an agent becomes traced if they undergo this transition
    def __init__(self, from_state, from_quar, to_quar, waiting_time):
        super().__init__(from_state, from_state, waiting_time)
        self.from_quar = from_quar
        self.to_quar = to_quar

