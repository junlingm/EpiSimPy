from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager


wait_exp = lambda rate: lambda _: random.exponential(1 / rate)

N=5000000
p = 0.3
beta = 0.4
gamma = 0.1
tau = 0.15
I0 = 20
theta = 10

runs = 100
save = True

def transmitted(time, sim, agent, from_state):
    l = agent[0].state["transmitted"]
    if agent[1] not in l:
        l.append(agent[1])
        agent[1].state["transmitted"].append(agent[0])

def trace(time, sim, agent, from_state):
    l = agent.state["transmitted"]
    agent.state["transmitted"] = list()
    for c in l:
        if c.state[None] == "I" and random.random_sample() < p:
            sim.set_state(time, c, State("T"))

init = lambda time, agent: State({"transmitted": []}) & State("I" if agent.id < I0 else "S")

def run(times):
    sim = Simulation("test", N)
    sim.set(Transition(State("I"), State("R"), wait_exp(gamma)))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + State("I"),
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("I"),
                       to_state=State("T"),
                       waiting_time=wait_exp(tau)))
    sim.set(Transition(from_state=State("T"),
                       to_state=State("X"),
                       waiting_time=wait_exp(theta),
                       changed_callback=trace))

    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(Counter(name="T", state=State("T")))
    sim.set(Counter(name="X", state=State("X")))
    sim.set(RandomMixing(sim, beta))
    sim.set(InitFunction(init))

    return sim.run(times)

start_time = time()
S = Averager()
I = Averager()
R = Averager()
T = Averager()
X = Averager()
for i in range(runs):
    print(i)
    v = run(range(250))
    S += v["S"]
    I += v["I"]
    R += v["R"]
    T += v["T"]
    X += v["X"]

t = v["times"]

end_time = time()

if save:
    import csv
    with open("SIR.p.{p:.1f}.csv".format(p=p), 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['t', "S", "I", "T", "X", "R"])
        print('t', "S", "I", "T", "X", "R")
        for i in range(len(v["times"])):
            w.writerow([t[i], S[i], I[i], T[i], X[i], R[i]])
            print(t[i], S[i], I[i], T[i], X[i], R[i])

print("--- %s seconds ---" % (end_time - start_time))
