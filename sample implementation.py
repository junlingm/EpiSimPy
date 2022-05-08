from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager

wait_exp = lambda rate: lambda _: random.exponential(1 / rate)
immediately = lambda _: 0

N = 10000
E0 = 20  # everyone is either exposed or susceptible at t_0

p = 0.1
f = 0.25
delta = 0.27
gamma_A = 0.1
gamma_I = 0.1177
sigma = 0.662
epsilon = 0  # need to define more transitions to change this
beta_A = 0.3
beta_P = 0.7
beta_I = 0.5
tau_I = 0.3  # rate at which an infected person gets tested
tau = 1 / 14

def transmissible(time, sim, agent, to_state):
    return random.random_sample() < agent[0].state["infectivity"]


def transmitted(time, sim, agent, from_state):
    l = agent[0].state["transmitted"]
    if agent[1] not in l:
        l.append(agent[1])

def trace(time, sim, agent, from_state):
    for c in agent.state["transmitted"]:
        if random.random_sample() < p:
            s = c.state[None]
            if s == "E":
                sim.set_state(time, c, {None: "QE"})
            elif s == "A":
                sim.set_state(time, c, {None: "QA", "infectivity": beta_A * epsilon})
            elif s == "P":
                sim.set_state(time, c, {None: "QP", "infectivity": beta_P * epsilon})
            elif s == "I":
                sim.set_state(time, c, {None: "T", "infectivity": 0})
                trace(time, sim, c, None)

init = lambda time, agent: State({"quarantined": False,
                                  "infectivity": 0,
                                  "transmitted": []}) & (State("E") if agent.id < E0 else State("S"))

def run(times):
    sim = Simulation("contact_tracing", N)
    # disease progression
    sim.set(Transition(from_state=State("E"),
                       to_state=State("A") & {"infectivity": beta_A},
                       waiting_time=wait_exp(f * delta)))
    sim.set(Transition(from_state=State("E"),
                       to_state=State("P") & {"infectivity": beta_P},
                       waiting_time=wait_exp((1 - f) * delta)))
    sim.set(Transition(from_state=State("A"),
                       to_state=State("R") & {"infectivity": 0},
                       waiting_time=wait_exp(gamma_A)))
    sim.set(Transition(from_state=State("P"),
                       to_state=State("I") & {"infectivity": beta_I},
                       waiting_time=wait_exp(sigma)))
    sim.set(Transition(from_state=State("I"),
                       to_state=State("R") & {"infectivity": 0},
                       waiting_time=wait_exp(gamma_I)))

    sim.set(Transition(from_state=State("I") + State("S"),
                       to_state=State("I") + State("E"),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("P") + State("S"),
                       to_state=State("P") + State("E"),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("QP") + State("S"),
                       to_state=State("P") + State("E"),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("A") + State("S"),
                       to_state=State("A") + State("E"),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("QA") + State("S"),
                       to_state=State("A") + State("E"),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    # testing
    sim.set(Transition(from_state=State("I"),
                       to_state=State("T") & {"infectivity": 0},
                       waiting_time=wait_exp(tau_I + tau),
                       changed_callback=trace))
    sim.set(Transition(from_state=State("A"),
                       to_state=State("T") & {"infectivity": 0},
                       waiting_time=wait_exp(tau),
                       changed_callback=trace))
    sim.set(Transition(from_state=State("P"),
                       to_state=State("T") & {"infectivity": 0},
                       waiting_time=wait_exp(tau),
                       changed_callback=trace))

    sim.set(Transition(from_state=State("QE"),
                       to_state=State("QA") & {"infectivity": beta_A * epsilon},
                       waiting_time=wait_exp(f * delta)))

    sim.set(Transition(from_state=State("QE"),
                       to_state=State("QP") & {"infectivity": beta_P * epsilon},
                       waiting_time=wait_exp((1 - f) * delta)))

    sim.set(Transition(from_state=State("QA"),
                       to_state=State("T") & {"infectivity": 0},
                       waiting_time=immediately,
                       changed_callback=trace))

    sim.set(Transition(from_state=State("QP"),
                       to_state=State("T") & {"infectivity": 0},
                       waiting_time=immediately,
                       changed_callback=trace))

    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="E", state=State("E")))
    sim.set(Counter(name="A", state=State("A")))
    sim.set(Counter(name="P", state=State("P")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="QE", state=State("QE")))
    sim.set(Counter(name="QA", state=State("QA")))
    sim.set(Counter(name="QP", state=State("QP")))
    sim.set(Counter(name="T", state=State("T")))
    sim.set(Counter(name="R", state=State("R")))

    sim.set(RandomMixing(sim, 1))
    sim.set(InitFunction(init))

    return sim.run(times)


start_time = time()
S = Averager()
E = Averager()
A = Averager()
P = Averager()
I = Averager()
QE = Averager()
QA = Averager()
QP = Averager()
T = Averager()
R = Averager()
for i in range(100):
    print("run", i)
    v = run(range(150))
    S += v["S"]
    E += v["E"]
    A += v["A"]
    P += v["P"]
    I += v["I"]
    QE += v["QE"]
    QA += v["QA"]
    QP += v["QP"]
    T += v["T"]
    R += v["R"]
t = v["times"]

end_time = time()
import csv

with open("sim.p.%1.1f.csv" % p, 'w') as csvfile:
    w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    w.writerow(['t', "S", "E", "A", "P", "I", "QE", "QA", "QP", "T", "R"])
    print('t', "S", "E", "A", "P", "I", "T", "QE", "QA", "QP", "R")
    for i in range(len(v["times"])):
        w.writerow([t[i], S[i], E[i], A[i], P[i], I[i], QE[i], QA[i], QP[i], T[i], R[i]])
        print(t[i], S[i], E[i], A[i], P[i], I[i], QE[i], QA[i], QP[i], T[i], R[i])
print("--- %s seconds ---" % (end_time - start_time))
