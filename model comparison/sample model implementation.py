from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
import matplotlib.pyplot as plt

N_0 = 10000
E_0 = 20  # everyone is either exposed or susceptible at t_0
f = 0.5
delta = 6
delta_Q = delta
gamma_A = 5
gamma_I = 5
sigma = 2
epsilon = 0  # need to define more transitions to change this
beta_A = 0.25
beta_P = 0.4
beta_I = 0.3
tau_I = 2  # rate at which an infected person gets tested
# theta_I, theta_A, theta_P = ?

def gen(i):
    if i < E_0:
        return Agent("E", number=i)
    return Agent("S", number=i)


# network = DegreeDistribution(100, lambda: random.randint(1, 20))
network = ER(N_0, 0.001)

per_edge_contact_rate = 0.2
trace_rate = 2
population = Population(N_0, gen, network.network, per_edge_contact_rate, trace_rate)

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]

# state = "I", quarantine = True
# these are states that are automatically traced

quar_period = 14

SIR = Simulation(states, traced_states, population, quar_period)

SIR.define(InfTrans(from_state="E", to_state="A",
                    waiting_time=lambda: np.random.exponential(f*delta)))
SIR.define(InfTrans(from_state="E", to_state="P",
                    waiting_time=lambda: np.random.exponential((1-f)*delta)))
SIR.define(InfTrans(from_state="A", to_state="R",
                    waiting_time=lambda: np.random.exponential(gamma_A)))
SIR.define(InfTrans(from_state="P", to_state="I",
                    waiting_time=lambda: np.random.exponential(sigma)))
SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(gamma_I)))
SIR.define(TestTrans(from_state="I", from_quar=False, to_quar=True,
                     waiting_time=lambda: np.random.exponential(tau_I)))

# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=False, chance=0.1))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=True, chance=0.01))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=False, chance=beta_A))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="A", contact_quar=True, chance=0.02))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=False, chance=beta_P))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="P", contact_quar=True, chance=0.06))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=False, chance=beta_I))
# SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=True, chance=0.1))

SIR.define(ClassTotal("S", N_0-E_0, "S"))
SIR.define(Total("Eu", E_0, "E", False))  # E unquarantined
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
# plt.plot(data["time"], data["S"], color="red")
#plt.plot(data["time"], data["S"], color="blue")
#plt.show()
