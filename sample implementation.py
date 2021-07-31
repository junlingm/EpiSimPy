from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
import matplotlib.pyplot as plt


def gen(i):
    if i < 20:
        return Agent("E", number=i)
    return Agent("S", number=i)


# network = DegreeDistribution(100, lambda: random.randint(1, 20))
network = ER(100, 0.1)

per_edge_contact_rate = 0.2
trace_rate = 10
population = Population(100, gen, network.network, per_edge_contact_rate, trace_rate)

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
# state = "I", quarantine = True
# these are states that are automatically traced

quar_period = 14

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

# SIR.define(Contact(from_state="S", to_state="E", contact_state="E", contact_quar=False, chance=0.1))
# SIR.define(Contact(from_state="S", to_state="E", contact_state="E", contact_quar=True, chance=0.01))
SIR.define(Contact(from_state="S", to_state="E", contact_state="A", contact_quar=False, chance=0.25))
# SIR.define(Contact(from_state="S", to_state="E", contact_state="A", contact_quar=True, chance=0.02))
SIR.define(Contact(from_state="S", to_state="E", contact_state="P", contact_quar=False, chance=0.4))
# SIR.define(Contact(from_state="S", to_state="E", contact_state="P", contact_quar=True, chance=0.06))
SIR.define(Contact(from_state="S", to_state="E", contact_state="I", contact_quar=False, chance=0.3))
# SIR.define(Contact(from_state="S", to_state="E", contact_state="I", contact_quar=True, chance=0.1))

SIR.define(ClassTotal("S", 80, "S"))
SIR.define(Total("Eu", 20, "E", False))  # E unquarantined
SIR.define(Total("Eq", 0, "E", True))  # E quarantined
SIR.define(Total("Iq", 0, "I", True))
SIR.define(ClassTotal("T", 0, "T"))
data = SIR.run(list(range(200)))

print("time: ", data["time"])
print("S: ", data["S"])
print("E unquarantined: ", data["Eu"])
print("E quarantined: ", data["Eq"])
# plt.plot(data["time"], data["S"], color="red")
plt.plot(data["time"], data["Iq"], color="blue")
plt.show()
