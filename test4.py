from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *

def gen(i):
    if i < 20:
        return Agent_network("I", number=i)
    return Agent_network("S", number=i)


global_contact_rate = 5
trace_prob = 1
trace_rate = None
network = ER(1000, 0.01)
population = Population_network(1000, gen, network.network, contact_rate=0.2, trace_rate=inf, trace_prob=0.9)

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