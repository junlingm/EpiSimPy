from simulation import *
from population import *
from transitions import *
from loggers import *
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)

N_0 = 10000
E_0 = 20  # everyone is either exposed or susceptible at t_0
f = 0.5
delta = 2/3
delta_Q = delta
gamma_A = 1/5
gamma_I = 1/5
sigma = 1/2
epsilon = 0  # need to define more transitions to change this
beta_A = 0.25
beta_P = 0.4
beta_I = 0.3
tau_I = 1/2  # rate at which an infected person gets tested
# theta_I, theta_A, theta_P = ?

quar_period = 14
periodic_test_interval = 14
quar_test_time = None


def gen(i, s):
    if i < E_0:
        return Agent("E", number=i, size=s)
    return Agent("S", number=i, size=s)


global_contact_rate = 2
trace_rate = 2
population = Population(N_0, gen, global_contact_rate, trace_rate)

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
SIR.define(Total("Eu", E_0, "E", False))  # E unquarantined
SIR.define(Total("Eq", 0, "E", True))  # E quarantined
SIR.define(Total("Iq", 0, "I", True))
SIR.define(Total("Iu", 0, "I", False))
SIR.define(ClassTotal("T", 0, "T"))
data = SIR.run(list(range(200)))

reps = 20

#trace_rates = [0.00001, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 1, 2, 5]
trace_rates = [0.00001, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.75, 1]
avgs = []
for rate in trace_rates:
    final_S = []
    print("new rate: ", rate)
    for _ in range(reps):
        print(_)
        SIR.population.trace_rate = rate
        data = SIR.run(list(range(200)))
        final_S.append(data["S"][-1])
    avgs.append(sum(final_S)/reps)

print(avgs)
#plt.plot([0, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 1, 2, 5], avgs)
plt.plot([0, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.75, 1], avgs)

plt.xlabel("test rate")
plt.ylabel("final susceptible count")
plt.title("random mixing with 14 day periodic testing")
plt.show()



