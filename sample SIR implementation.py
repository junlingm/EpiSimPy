from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *


def gen(i):
    li = [i for i in range(100)]
    li.remove(i)
    if i < 20:
        return Agent("I", number=i)
    return Agent("S", number=i)


# network = DegreeDistribution(1000, lambda: random.randint(1, 20))
network = ER(100, 0.1)
per_edge_contact_rate = 0.02
trace_rate = 20
population = Population(100, gen, network.network, per_edge_contact_rate, trace_rate)

states = ["S", "I", "R"]
traced_states = []
quar_period = 0.0001

SIR = Simulation(states, traced_states, population, quar_period)


SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(10)))


SIR.define(Contact(from_state="S", to_state="I", contact_state="I", contact_quar=False, chance=1))


SIR.define(ClassTotal("S", 80, "S"))
SIR.define(ClassTotal("I", 20, "I"))
data = SIR.run(list(range(100)))

print("time: ", data["time"])
print("S: ", data["S"])
print("I: ", data["I"])
