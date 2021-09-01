from simulation import *
from population import *
from transitions import *
from loggers import *
import matplotlib.pyplot as plt
import sys
from math import inf
#import threading
from averagers import *

sys.setrecursionlimit(100000)
#threading.stack_size(200000000)

p = 0.5
N_0 = 10000
E_0 = 20  # everyone is either exposed or susceptible at t_0
f = 0.25
delta = 0.27
delta_Q = delta
gamma_A = 0.1
gamma_I = 0.1177
sigma = 0.662
epsilon = 0  # need to define more transitions to change this
beta_A = 0.3
beta_P = 0.7
beta_I = 0.5
tau_I = 0.3  # rate at which an infected person gets tested
tau = 1/14
# theta_I, theta_A, theta_P = ?


quar_period = 14
if tau == 0:
    periodic_test_interval = None
else:
    periodic_test_interval = 1/tau
quar_test_time = None


def gen(i, s):
    if i < E_0:
        return Agent("E", number=i, size=s)
    return Agent("S", number=i, size=s)


global_contact_rate = 1
trace_rate = inf
population = Population(N_0, gen, global_contact_rate, trace_rate, trace_prob=p)

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
pos_test = ["P", "I", "A"]

# state = "I", quarantine = True
# these are states that are automatically traced

SIR = Simulation(states, traced_states, population, quar_period, pos_test, quar_test_time, periodic_test_interval)

SIR.define(InfTrans(from_state="E", to_state="A",
                    waiting_time=lambda: np.random.exponential(1/(f * delta))))
SIR.define(InfTrans(from_state="E", to_state="P",
                    waiting_time=lambda: np.random.exponential(1/((1 - f) * delta))))
SIR.define(InfTrans(from_state="A", to_state="R",
                    waiting_time=lambda: np.random.exponential(1/gamma_A)))
SIR.define(InfTrans(from_state="P", to_state="I",
                    waiting_time=lambda: np.random.exponential(1/sigma)))
SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(1/gamma_I)))
SIR.define(TestTrans(from_state="I", from_quar=False, to_quar=True,
                     waiting_time=lambda: np.random.exponential(1/tau_I)))

# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=False, chance=0.1))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=True, chance=0.01))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=False, chance=beta_A))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="A", contact_quar=True, chance=0.02))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=False, chance=beta_P))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="P", contact_quar=True, chance=0.06))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=False, chance=beta_I))
# SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=True, chance=0.1))

SIR.define(ClassTotal("S", N_0 - E_0, "S"))
SIR.define(ClassTotal("E", E_0, "E"))
SIR.define(ClassTotal("P", 0, "P"))
SIR.define(ClassTotal("A", 0, "A"))
SIR.define(ClassTotal("I", 0, "I"))
SIR.define(ClassTotal("R", 0, "R"))
SIR.define(Total("Eq", 0, "E", True))
SIR.define(Total("Aq", 0, "A", True))
SIR.define(Total("Pq", 0, "P", True))

reps = 20



sims_S = []
sims_E = []
sims_P = []
sims_I = []
sims_A = []
sims_R = []
sims_Eq = []
sims_Aq = []
sims_Pq = []
for _ in range(reps):
    print(_)
    data = SIR.run(list(range(500)))
    sims_S.append(data["S"])
    sims_E.append(data["E"])
    sims_P.append(data["P"])
    sims_I.append(data["I"])
    sims_A.append(data["A"])
    sims_R.append(data["R"])
    sims_Eq.append(data["Eq"])
    sims_Aq.append(data["Aq"])
    sims_Pq.append(data["Pq"])
print(data["time"])
print(sims_Aq)
sims_S = averager(sims_S)
sims_E = averager(sims_E)
#print("max E", max(sims_E)/N_0)
sims_P = averager(sims_P)
sims_I = averager(sims_I)
sims_A = averager(sims_A)
#print("max A", max(sims_A)/N_0)
sims_R = averager(sims_R)
sims_Eq = averager(sims_Eq)
sims_Aq = averager(sims_Aq)
sims_Pq = averager(sims_Pq)
print(sims_S)
print(sims_E)
print(sims_P)
print(sims_I)
print(sims_A)

print(sims_R)
print("break")
print(sims_Eq)
print(sims_Aq)
print(sims_Pq)
plt.plot(range(500), sims_S)
plt.show()
