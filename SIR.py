from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time


wait_exp = lambda rate: lambda _: random.exponential(1 / rate)

N=10000
beta = 0.4
gamma = 0.2
I0 = 5

save = False
#save = True

def init(time, agent):
    if agent.id < I0:
        s = "I"
    else:
        s = "S"
    return State(s)

def run(times):
    sim = Simulation("test", N)
    rm = RandomMixing(sim)
    sim.set(rm)
    sim.set(Transition(State("I"), State("R"), wait_exp(gamma)))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + State("I"),
                       wait_exp(beta), contact=rm))

    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(InitFunction(init))

    return sim.run(times)


start_time = time()
v = run(range(101))
end_time = time()

t = v["times"]

print('t', "S", "I", "R")
for i in range(len(t)):
    print(t[i], v["S"][i], v["I"][i], v["R"][i])

if save:
    import csv
    with open("SEIR.csv", 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['t', "S", "E", "I", "R"])
        for i in range(len(v["times"])):
            w.writerow([t[i], v["S"][i], v["E"][i], v["I"][i], v["R"][i]])
print("--- %s seconds ---" % (end_time - start_time))
