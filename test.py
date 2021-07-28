import matplotlib.pyplot as plt
from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
from comparisons.ODE_model import *

N = 100
I_0 = 20
beta = 0.02
ER_p = 0.1
lambd = (N - 1) * ER_p
gamma = 1 / 10
dt = 0.01

def gen(i):
    if i < I_0:
        return Agent("I", number=i)
    return Agent("S", number=i)


network = ER(N, ER_p)
trace_rate = None
population = Population(N, gen, network.network, beta, trace_rate)
states = ["S", "I", "R"]
traced_states = []
quar_period = None
SIR = Simulation(states, traced_states, population, quar_period)
SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(1 / gamma)))
SIR.define(Contact(from_state="S", to_state="I", contact_state="I", contact_quar=False, chance=1))
SIR.define(ClassTotal("S", N - I_0, "S"))

sim = SIR.run(list(range(100)))
print(sim["time"])
print(sim["S"])

plt.plot(sim["time"], sim["S"])

DE = ODE(N, I_0, beta, lambd, gamma, dt)
plt.plot(range(100), DE)
plt.show()

