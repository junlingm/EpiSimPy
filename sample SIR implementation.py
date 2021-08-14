from simulation import *
from population import *
from transitions import *
from numpy import random
from time import time
from averagers import Averager


wait_exp = lambda scale: lambda _: random.exponential(scale)

N=10000
beta = 0.3
gamma = 0.2
I0 = 10

def transmissible(time, sim, agent, to_state):
    v = random.random_sample()
    return v < agent[0].state["infectivity"] * agent[1].state["susceptibility"]

def run(times):
    sim = Simulation("test", N)
    sim.set(Transition(State("I"), State("R"), wait_exp(1/gamma)))
    sim.set(Transition(State("I") + State("S"),
                       State("I") + (State("I") & {"infectivity":1}),
                       to_change_callback=transmissible))
    sim.set(Counter(name="S", state=State("S")))
    sim.set(Counter(name="I", state=State("I")))
    sim.set(Counter(name="R", state=State("R")))
    sim.set(RandomMixing(sim, beta))
    sim.set(InitFunction(lambda time, agent: State("I") & {"susceptibility":0, "infectivity":1}
        if agent.id < I0 else State("S") & {"susceptibility":1, "infectivity":0}))

    return sim.run(times)

start_time = time()
S = Averager()
I = Averager()
R = Averager()
for i in range(100):
    v = run(range(150))
    S += v["S"]
    I += v["I"]
    R += v["R"]
t = v["times"]

end_time = time()
for i in range(len(v["times"])):
    print(t[i], S[i], I[i], R[i])

print("--- %s seconds ---" % (end_time - start_time))
