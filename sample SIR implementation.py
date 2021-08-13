from simulation import *
from population import *
from agent import *
from transitions import *
from numpy import random
from time import time
# import cProfile


wait_exp = lambda scale: lambda _: random.exponential(scale)

N=10000
beta = 0.3
gamma = 0.2
I0 = 10

def to_contact(time, sim, agent, to_state):
    v = random.random_sample()
    return v < agent[0].state["infectivity"] * agent[1].state["susceptibility"]

def run(times):
    sim = Simulation("test", N)
    sim.set(Transition(State("I", "infection"), State("R", "infection"), wait_exp(1/gamma)))
    sim.set(Transition(State("I", "infection") + State("S", "infection"),
                       State("I", "infection") + State({"infection":"I", "infectivity":1}),
                       to_change_callback=to_contact))
    sim.set(Counter(name="S", state=State("S", "infection")))
    sim.set(Counter(name="I", state=State("I", "infection")))
    sim.set(Counter(name="R", state=State("R", "infection")))
    sim.set(RandomMixing(sim, beta))
    sim.set(InitFunction(lambda time, agent: State({"infection":"I", "susceptibility":0, "infectivity":1}) \
        if agent.id < I0 else State({"infection":"S", "susceptibility":1, "infectivity":0})))

    return sim.run(times)

start_time = time()
# cProfile.run("v = run(range(150))")
v = run(range(150))

for i in range(len(v["times"])):
    print(v["times"][i], v["S"][i], v["I"][i])

print("--- %s seconds ---" % (time() - start_time))
