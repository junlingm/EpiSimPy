from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *


def gen(i):
    if i < 20:
        return Agent("I", number=i)
    return Agent("S", number=i)


# network = DegreeDistribution(1000, lambda: random.randint(1, 20))
network = ER(1000, 0.01)
per_edge_contact_rate = 0.02
trace_rate = None
population = Population(1000, gen, network.network, per_edge_contact_rate, trace_rate)

states = ["S", "I", "R"]
traced_states = []
quar_period = None
SIR = Simulation(states, traced_states, population, quar_period, ["I"], None, None)


SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(10)))


SIR.define(Contact(from_state="S", to_state="I", self_quar=False, contact_state="I", contact_quar=False, chance=1))


SIR.define(ClassTotal("S", 980, "S"))
SIR.define(ClassTotal("I", 20, "I"))
data = SIR.run(list(range(100)))

print("time: ", data["time"])
print("S: ", data["S"])
print("I: ", data["I"])
