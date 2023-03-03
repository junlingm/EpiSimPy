from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager


wait_exp = lambda rate: lambda _: random.exponential(1 / rate)
def wait_exp2(rate1, rate2, T):
    def waiting_time(time):
        if time > T:
            return random.exponential(1 / rate2)
        t = random.exponential(1 / rate1)
        if time + t < T:
            return t
        return T - time + random.exponential(1 / rate2)
    return waiting_time

N=50000
p = 0.2
q = 0.3
# Tc is the time of the control measure set to None for no control
Tc  = 30
beta_I = 0.6
beta_A = 0.2
sigma=0.27
gamma = 0.1
gamma_A=0.2
tau = 0.15
I0 = 20
theta = 2
t1=79
runs = 1
save = True

if Tc is not None:
    eps = 0.5
    beta_I2 = beta_I * eps
    beta_A2 = beta_A * eps
    wt_I = wait_exp2(beta_I, beta_I2, Tc)
    wt_A = wait_exp2(beta_A, beta_A2, Tc)
else:
    wt_I = wait_exp(beta_I)
    wt_A = wait_exp(beta_A)


def transmitted(time, sim, agent, from_state):
    l = agent[0].state["transmitted"]
    if agent[1] not in l:
        l.append(agent[1])
        agent[1].state["transmitted"].append(agent[0])


def trace(time, sim, agent, from_state):
    l = agent.state["transmitted"]
    agent.state["transmitted"] = list()
    for c in l:
        if random.random_sample() < p:
            if c.state[None] == "I":
                sim.set_state(time, c, State("T"))
            elif c.state[None] == "E":
                sim.set_state(time, c, State("Q"))
            elif c.state[None] == "A":
                sim.set_state(time, c, State("QA"))

init = lambda time, agent: State({"transmitted": []}) & State("I" if agent.id < I0 else "S")

def run(times):
    sim = Simulation("test", N)
    rm = RandomMixing(sim)
    sim.set(rm)
    sim.set(Transition(State("A"), State("R"), wait_exp(gamma_A)))
    sim.set(Transition(State("QA"), State("R"), wait_exp(gamma_A)))
    sim.set(Transition(State("Q"), State("T"), wait_exp(sigma*(1-q))))
    sim.set(Transition(State("Q"), State("QA"), wait_exp(sigma * q)))
    sim.set(Transition(State("E"), State("I"), wait_exp(sigma*(1-q))))
    sim.set(Transition(State("E"), State("A"), wait_exp(sigma*q)))
    sim.set(Transition(State("I"), State("R"), wait_exp(gamma)))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + State("E"),
                       contact=rm,
                       waiting_time=wt_I,
                       # waiting_time=wait_exp(beta_I),
                       changed_callback=transmitted))
    sim.set(Transition(State("A") + State("S"),
                       State("A") + State("E"),
                       contact=rm,
                       waiting_time=wt_A,
                       # waiting_time=wait_exp(beta_A),
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("I"),
                       to_state=State("T"),
                       waiting_time=wait_exp(tau)))
    sim.set(Transition(from_state=State("T"),
                       to_state=State("X"),
                       waiting_time=wait_exp(theta),
                       changed_callback=trace))

    sim.set(Counter(name="infection", state=State("S"), to_state=State("E")))
    sim.set(Counter(name="quarantine", state=State("E"), to_state=State("Q")))
    sim.set(Counter(name="Asymptomatic_Quarantine", state=State("A"), to_state=State("QA")))
    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(Counter(name="T", state=State("T")))
    sim.set(Counter(name="X", state=State("X")))
    sim.set(InitFunction(init))

    return sim.run(times)


start_time = time()
S = Averager()
I = Averager()
R = Averager()
T = Averager()
X = Averager()
Quarantine = Averager()

v = run(range(250))
S += v["S"]
I += v["I"]
R += v["R"]
T += v["T"]
X += v["X"]
Quarantine += v["quarantine"]

t = v["times"]

end_time = time()

Sm = S.mean()
Im = I.mean()
Tm = T.mean()
Xm = X.mean()
Rm = R.mean()
Qm = Quarantine.mean()

print('t', "S", "I", "T", "X", "R", "Q")
for i in range(len(t)):
    print(t[i], Sm[i], Im[i], Tm[i], Xm[i], Rm[i], Qm[i])

if save:
    import csv
    with open("SIR.p.{p:.1f}.csv".format(p=p), 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['t', "S", "I", "T", "X", "R", "Q"])
        for i in range(len(v["times"])):
            w.writerow([t[i], Sm[i], Im[i], Tm[i], Xm[i], Rm[i], Qm[i]])


print("--- %s seconds ---" % (end_time - start_time))