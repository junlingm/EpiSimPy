from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
import matplotlib.pyplot as plt
from averagers import *

def gen(i):
    if i < 20:
        return Agent("E", number=i)
    return Agent("S", number=i)


# network = DegreeDistribution(100, lambda: random.randint(1, 20))

per_edge_contact_rate = 0.2
trace_rate = 2

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
pos_test = ["E", "P", "I", "A"]
# state = "I", quarantine = True
# these are states that are automatically traced

quar_period = 14

test_time = lambda: 2

reps = 50

results = []
for _ in range(reps):
    print(_)
    network = ER(10000, 0.001)
    population = Population(10000, gen, network.network, per_edge_contact_rate, trace_rate)
    test_time = lambda: 2
    SIR = Simulation(states, traced_states, population, quar_period, pos_test, test_time)
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
    data = SIR.run(list(range(200)))
    results.append(data["S"])
avgs = averager(results)

print(avgs)
plt.plot(range(200), avgs)
plt.xlabel("time")
plt.ylabel("susceptible count")
plt.title("with test results 2 days after the start of quarantine")
plt.show()