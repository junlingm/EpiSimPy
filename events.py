
class ContactEvent:
    def __init__(self, person, contacter):
        self.contacter = contacter
        self.person = person 


class SelfEvent:
    def __init__(self, person, transition):
        self.person = person
        self.transition = transition


class TraceEvent:
    def __init__(self, person, contact):
        self.person = person
        self.contact = contact


class UpdateEvent:
    def __init__(self, done=False):
        self.end_sim = done
