from simulation import *
from population import *
from transitions import *
from loggers import *
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)

def gen(i, s):
    if i < 20:
        return Agent("E", number=i, size=s)
    return Agent("S", number=i, size=s)


global_contact_rate = 2
trace_rate = 0.00001
population = Population(10000, gen, global_contact_rate, trace_rate)

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
pos_test = ["P", "I", "A"]

quar_period = 14

SIR = Simulation(states, traced_states, population, quar_period, pos_test,
                 quar_test_time=None, periodic_test_interval=14)

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

# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=False, chance=0.1))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=True, chance=0.01))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=False, chance=0.25))
#SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=True, chance=0.025))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=False, chance=0.4))
#SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=True, chance=0.04))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=False, chance=0.3))
#SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=True, chance=0.03))

SIR.define(ClassTotal("S", 9980, "S"))
SIR.define(Total("Eu", 20, "E", False))  # E unquarantined
SIR.define(Total("Eq", 0, "E", True))  # E quarantined
SIR.define(Total("Iq", 0, "I", True))
SIR.define(Total("Iu", 0, "I", False))
SIR.define(ClassTotal("T", 0, "T"))
data = SIR.run(list(range(200)))

print("time: ", data["time"])
print("S: ", data["S"])
print("E unquarantined: ", data["Eu"])
print("E quarantined: ", data["Eq"])
print("I unquarantined: ", data["Iu"])
print("I quarantined: ", data["Iq"])
print("final susceptible count:", data["S"][-1])
plt.plot(data["time"], data["S"], color="blue")
plt.show()
