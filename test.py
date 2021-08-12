
from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
from averagers import *
import matplotlib.pyplot as plt


def gen(i):
    if i < 20:
        return Agent("E", number=i)
    return Agent("S", number=i)

per_edge_contact_rate = 0.2
trace_rate = 10


states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
# state = "I", quarantine = True
# these are states that are automatically traced

quar_period = 14

reps = 50
results = []
for _ in range(reps):
    print(_)
    network = ER(10000, 0.001)

    population = Population(10000, gen, network.network, per_edge_contact_rate, trace_rate)

    SIR = Simulation(states, traced_states, population, quar_period)

    SIR.define(InfTrans(from_state="E", to_state="A",
                        waiting_time=lambda: np.random.exponential(3)))
    SIR.define(InfTrans(from_state="E", to_state="P",
                        waiting_time=lambda: np.random.exponential(3)))
    SIR.define(InfTrans(from_state="A", to_state="R",
                        waiting_time=lambda: np.random.exponential(5)))
    SIR.define(InfTrans(from_state="P", to_state="I",
                        waiting_time=lambda: np.random.exponential(2)))
    SIR.define(InfTrans(from_state="I", to_state="R",
                        waiting_time=lambda: np.random.exponential(5)))
    SIR.define(TestTrans(from_state="I", from_quar=False, to_quar=True,
                         waiting_time=lambda: np.random.exponential(2)))
    SIR.define(
        Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=False, chance=0.25))
    SIR.define(
        Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=False, chance=0.4))
    SIR.define(
        Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=False, chance=0.3))
    SIR.define(ClassTotal("S", 9980, "S"))
    data = SIR.run(range(200))
    results.append(data["S"])
avgs = averager(results)
plt.plot(range(200), avgs)
plt.xlabel("time")
plt.ylabel("susceptibles")
plt.title("control simulation")
plt.show()

