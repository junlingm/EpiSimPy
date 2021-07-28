import time
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from ODE_model import *
from simulation import *
from population import *
from transitions import *
from loggers import *
from networks import *
from averagers import *

start_time = time.time()

N = 10000
I_0 = 20
beta = 0.02
ER_p = 0.001
lambd = (N - 1) * ER_p
gamma = 1 / 10
dg = lambda x: math.exp(lambd * (x - 1)) * lambd
ddg = lambda x: math.exp(lambd * (x - 1)) * lambd ** 2


def Miller(t, r):
    x, y, S = r
    fx = -beta * y
    fy = -beta * y - gamma * y + beta * y * ddg(x) / dg(1)
    fS = -beta * y * dg(x) * N
    return fx, fy, fS


sol = solve_ivp(Miller, [0, 100], [1, I_0 / N, N - I_0],
                t_eval=range(100))

x, y, avg_2 = sol.y
plt.plot(sol.t, avg_2)


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
                    waiting_time=lambda: np.random.exponential(1/gamma)))
SIR.define(Contact(from_state="S", to_state="I", contact_state="I", contact_quar=False, chance=1))
SIR.define(ClassTotal("S", N - I_0, "S"))

reps = 100
data_1 = []
for _ in range(reps):
    sim = SIR.run(list(range(100)))
    data_1.append(sim["S"])
    # print(sim["S"][-1])
avg_1 = averager(data_1)

for _ in range(len(avg_1), 100):
    avg_1.append(avg_1[-1])

plt.plot(range(100), avg_1, color="red")
plt.plot(range(100), avg_2, color="blue")
print("time elapsed: ", time.time()-start_time)
plt.show()

