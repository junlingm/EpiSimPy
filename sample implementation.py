from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager

wait_exp = lambda rate: lambda _: random.exponential(1 / rate)
immediately = lambda _: 0

N = 10000
beta_A = 0.3
beta_P = 0.5
beta_I = 0.7
delta = 0.2
sigma = 0.3
gamma_I = 0.11
gamma_A = 0.1
f = 0.2

tau = 1 / 14
tau_I = 1 / 2

I0 = 10
p = 1

def transmissible(time, sim, agent, to_state):
    v = random.random_sample()
    return v < agent[0].state["infectivity"] * agent[1].state["susceptibility"]


def transmitted(time, sim, agent, from_state):
    l = agent[0].state["transmitted"]
    if agent[1] not in l:
        l.append(agent[1])


def trace(time, sim, agent, from_state):
    for c in agent.state["transmitted"]:
        if random.random_sample() < p:
            sim.set_state(time, c, {"quarantined": True, "infectivity": 0, "susceptibility": 0})


def run(times):
    sim = Simulation("contact_tracing", N)
    # disease progression
    sim.set(Transition(from_state=State("E"), to_state=State("A") & {"infectivity": beta_A},
                       waiting_time=wait_exp(f * delta)))
    sim.set(Transition(from_state=State("E"), to_state=State("P") & {"infectivity": beta_P},
                       waiting_time=wait_exp((1 - f) * delta)))
    sim.set(Transition(from_state=State("A"), to_state=State("R") & {"infectivity": 0},
                       waiting_time=wait_exp(gamma_A)))
    sim.set(Transition(from_state=State("P"), to_state=State("I") & {"infectivity": beta_I},
                       waiting_time=wait_exp(sigma)))
    sim.set(Transition(from_state=State("I"), to_state=State("R") & {"infectivity": 0},
                       waiting_time=wait_exp(gamma_I)))
    # transmission
    sim.set(Transition(from_state=State("I") + State("S"),
                       to_state=State("I") + (State("E") & {"susceptibility": 0}),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("P") + State("S"),
                       to_state=State("P") + (State("E") & {"susceptibility": 0}),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    sim.set(Transition(from_state=State("A") + State("S"),
                       to_state=State("A") + (State("E") & {"susceptibility": 0}),
                       to_change_callback=transmissible,
                       changed_callback=transmitted))
    # testing
    sim.set(Transition(from_state=State("I") & {"positive": False},
                       to_state=State("I") & {"positive": True},
                       waiting_time=wait_exp(tau_I + tau),
                       changed_callback=trace))
    sim.set(Transition(from_state=State("A") & {"positive": False},
                       to_state=State("A") & {"positive": True},
                       waiting_time=wait_exp(tau),
                       changed_callback=trace))
    sim.set(Transition(from_state=State("P") & {"positive": False},
                       to_state=State("P") & {"positive": True},
                       waiting_time=wait_exp(tau),
                       changed_callback=trace))

    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="E", state=State("E")))
    sim.set(Counter(name="A", state=State("A")))
    sim.set(Counter(name="P", state=State("P")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="T", state=State({"positive":True})))

    sim.set(RandomMixing(sim, 1))
    sim.set(InitFunction(lambda time, agent: State({"quarantined": False,
                                                    "positive": False,
                                                    "transmitted": []}) &
                                             ((State("I") & {"susceptibility": 0, "infectivity": 1}) if
    agent.id < I0 else State("S") & {"susceptibility": 1, "infectivity": 0})))

    return sim.run(times)


start_time = time()
S = Averager()
E = Averager()
A = Averager()
P = Averager()
I = Averager()
T = Averager()
for i in range(10):
    print("run", i)
    v = run(range(150))
    S += v["S"]
    E += v["E"]
    A += v["A"]
    P += v["P"]
    I += v["I"]
    T += v["T"]
t = v["times"]

end_time = time()
for i in range(len(v["times"])):
    print(t[i], S[i], E[i], A[i], P[i], I[i], T[i])

print("--- %s seconds ---" % (end_time - start_time))
