class Logger:
    def __init__(self, name, initial):
        self.name = name
        self.value = initial
        self.initial = initial

    def log(self, from_state, to_state, from_quar, to_quar, from_test, to_test):
        pass

    def reset(self):
        self.value = self.initial


class Total(Logger):
    def __init__(self, name, initial, state, quar, test):
        super().__init__(name, initial)
        self.state = state
        self.quar = quar
        # quarantine status, True or False
        self.test = test
        # test status, True or False

    def log(self, from_state, to_state, from_quar, to_quar, from_test, to_test):
        if from_state == self.state and from_quar == self.quar and from_test == self.test:
            self.value -= 1
        if to_state == self.state and to_quar == self.quar and to_test == self.test:
            self.value += 1
# tracks a specific quarantine, infectious, and test state


class QuarClassTotal(Logger):
    def __init__(self, name, initial, state, quar):
        super().__init__(name, initial)
        self.state = state
        self.quar = quar

    def log(self, from_state, to_state, from_quar, to_quar, from_test, to_test):
        if from_state == self.state and from_quar == self.quar:
            self.value -= 1
        if to_state == self.state and to_quar == self.quar:
            self.value += 1
# tracks a specific quarantine and infectious state


class ClassTotal(Logger):
    def __init__(self, name, initial, state):
        super().__init__(name, initial)
        self.state = state

    def log(self, from_state, to_state, from_quar, to_quar, from_test, to_test):
        if from_state == self.state:
            self.value -= 1
        if to_state == self.state:
            self.value += 1
# tracks a specific infectious state
