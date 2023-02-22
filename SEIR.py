from simulation import *
from population import *
from transitions import *
from numpy import random


wait_exp = lambda rate: lambda _: random.exponential(1 / rate)

N=5000000
beta = 0.5
infectious = lambda _: random.gamma(4, 1)
latent = lambda _: random.gamma(5, 1)
I0 = 20
E0 = 20

control_measures = [(0, 1), (40, 0.8), (60, 0.6), (80, 0.4), (100, 0.6)]
def eps(time):
    n = len(control_measures) - 1
    for i in range(n):
        if control_measures[i][0] <= time < control_measures[i+1][0]:
            return control_measures[i][1]
    return control_measures[n][1]

#save = False
save = True

def to_transmit(time, sim, agent, from_state):
    return random.rand() < eps(time)

def init(time, agent):
    if agent.id < E0:
        s = "E"
    elif agent.id < I0 + E0:
        s = "I"
    else:
        s = "S"
    return State({"transmitted": []}) & State(s)

def run(times):
    sim = Simulation("test", N)
    rm = RandomMixing(sim)
    sim.set(rm)
    sim.set(Transition(State("E"), State("I"), latent))
    sim.set(Transition(State("I"), State("R"), infectious))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + State("E"),
                       waiting_time=wait_exp(beta),
                       to_change_callback=to_transmit,
                       contact = rm))

    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="E", state=State("E")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(InitFunction(init))

    return sim.run(times)


v = run(range(250))

t = v["times"]

print('t', "S", "E", "I", "R")
for i in range(len(t)):
    print(t[i], v["S"][i], v["E"][i], v["I"][i], v["R"][i])

if save:
    import csv
    with open("SEIR.csv", 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['t', "S", "E", "I", "R"])
        for i in range(len(v["times"])):
            w.writerow([t[i], v["S"][i], v["E"][i], v["I"][i], v["R"][i]])
