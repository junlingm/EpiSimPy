import matplotlib.pyplot as plt
from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
from comparisons.ODE_model import *
from averagers import averager

N = 20000
I_0 = 50
beta = 0.02
ER_p = 0.0005
lambd = (N - 1) * ER_p
gamma = 1 / 10
dt = 0.001

def gen(i):
    if i < I_0:
        return Agent("I", number=i)
    return Agent("S", number=i)


trace_rate = None
states = ["S", "I", "R"]
traced_states = []
quar_period = None

data = []

network = ER(N, ER_p)
population = Population(N, gen, network.network, beta, trace_rate)
for i in range(400):
    print("run", i)
    SIR = Simulation(states, traced_states, population, quar_period)
    SIR.define(InfTrans(from_state="I", to_state="R",
                        waiting_time=lambda: np.random.exponential(1 / gamma)))
    SIR.define(Contact(from_state="S", to_state="I", contact_state="I", contact_quar=False, chance=1))
    SIR.define(ClassTotal("S", N - I_0, "S"))
    sim = SIR.run(list(range(200)))
    data += [sim["S"]]

stoch = averager(data)
DE = ODE(N, I_0, beta, lambd, gamma, 200, dt)

print(stoch)
print(DE)

plt.plot(range(len(stoch)), stoch, '-r')
plt.plot(range(len(DE)), DE, '-b')
plt.show()
