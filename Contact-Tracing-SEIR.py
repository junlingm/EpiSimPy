from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager


wait_exp = lambda rate: lambda _: random.exponential(1 / rate)

N=50000
p = 0.2
beta = 0.6
sigma=0.27
gamma = 0.1
tau = 0.15
I0 = 20
theta = 10

runs = 1
save = False

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
            state = c.state[None]
            if state == "I":
                sim.set_state(time, c, State("T"))
            elif state == "E":
                sim.set_state(time, c, State("Q"))

init = lambda time, agent: State({"transmitted": []}) & State("I" if agent.id < I0 else "S")

def run(times):
    sim = Simulation("test", N)
    rm = RandomMixing(sim)
    sim.set(rm)
    sim.set(Transition(State("Q"), State("T"), wait_exp(sigma)))
    sim.set(Transition(State("E"), State("I"), wait_exp(sigma)))
    sim.set(Transition(State("I"), State("R"), wait_exp(gamma)))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + State("E"),
                       waiting_time=wait_exp(beta),
                       changed_callback=transmitted,
                       contact=rm))
    sim.set(Transition(from_state=State("I"),
                       to_state=State("T"),
                       waiting_time=wait_exp(tau)))
    sim.set(Transition(from_state=State("T"),
                       to_state=State("X"),
                       waiting_time=wait_exp(theta),
                       changed_callback=trace))

    sim.set(Counter(name="infection", state=State("S"), to_state=State("E")))
    sim.set(Counter(name="quarantine", state=State("E"), to_state=State("Q")))
    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="E", state=State("E")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(Counter(name="T", state=State("T")))
    sim.set(Counter(name="X", state=State("X")))
    sim.set(InitFunction(init))

    return sim.run(times)


start_time = time()
S = Averager()
E = Averager()
I = Averager()
R = Averager()
T = Averager()
X = Averager()
Quarantine = Averager()
for i in range(runs):
    print(i)
    v = run(range(250))
    S += v["S"]
    E += v["E"]
    I += v["I"]
    R += v["R"]
    T += v["T"]
    X += v["X"]
    Quarantine += v["quarantine"]

t = v["times"]

end_time = time()

Sm = S.mean()
Em = E.mean()
Im = I.mean()
Tm = T.mean()
Xm = X.mean()
Rm = R.mean()
Qm = Quarantine.mean()

print('t', "S", "E", "I", "T", "X", "R", "Qm")
for i in range(len(t)):
    print(t[i], Sm[i], Em[i], Im[i], Tm[i], Xm[i], Rm[i], Qm[i])

if save:
    import csv
    with open("SEIQTR.csv", "w") as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['t', "S", "I", "T", "X", "R", "curve"])
        for i in range(len(v["times"])):
            w.writerow([t[i], Sm[i], Im[i], Tm[i], Xm[i], Rm[i], "mean"])
        Sm = S.quantile(0.025)
        Im = I.quantile(0.025)
        Tm = T.quantile(0.025)
        Xm = X.quantile(0.025)
        Rm = R.quantile(0.025)
        for i in range(len(v["times"])):
            w.writerow([t[i], Sm[i], Im[i], Tm[i], Xm[i], Rm[i], "2.5% quantile"])
        Sm = S.quantile(0.975)
        Im = I.quantile(0.975)
        Tm = T.quantile(0.975)
        Xm = X.quantile(0.975)
        Rm = R.quantile(0.975)
        for i in range(len(v["times"])):
            w.writerow([t[i], Sm[i], Im[i], Tm[i], Xm[i], Rm[i], "97.5% quantile"])

print("--- %s seconds ---" % (end_time - start_time))
