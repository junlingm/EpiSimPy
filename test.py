
from simulation import *
from population import *
from transitions import *
from loggers import *
import matplotlib.pyplot as plt


def gen(i, s):
    if i < 20:
        return Agent("E", number=i, size=s)
    return Agent("S", number=i, size=s)


global_contact_rate = 0.2
trace_rate = 10
population = Population(10000, gen, global_contact_rate, trace_rate)

states = ["S", "E", "P", "I", "A", "R"]
traced_states = [("I", True)]
# state = "I", quarantine = True
# these are states that are automatically traced

quar_period = 14

SIR = Simulation(states, traced_states, population, quar_period)

SIR.define(InfTrans(from_state="E", to_state="A",
                    waiting_time=lambda: np.random.exponential(3)))
SIR.define(InfTrans(from_state="E", to_state="P",
                    waiting_time=lambda: np.random.exponential(3)))
SIR.define(InfTrans(from_state="A", to_state="R",
                    waiting_time=lambda: np.random.exponential(5)))
SIR.define(InfTrans(from_state="P", to_state="I",
                    waiting_time=lambda: np.random.exponential(2)))
SIR.define(InfTrans(from_state="I", to_state="R",
                    waiting_time=lambda: np.random.exponential(5)))
SIR.define(TestTrans(from_state="I", from_quar=False, to_quar=True,
                     waiting_time=lambda: np.random.exponential(2)))

# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=False, chance=0.1))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="E", contact_quar=True, chance=0.01))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="A", contact_quar=False, chance=0.25))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="A", contact_quar=True, chance=0.02))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="P", contact_quar=False, chance=0.4))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="P", contact_quar=True, chance=0.06))
SIR.define(Contact(from_state="S", to_state="E", self_quar=False, contact_state="I", contact_quar=False, chance=0.3))
# SIR.define(Contact(from_state="S", to_state="E",self_quar=False, contact_state="I", contact_quar=True, chance=0.1))

SIR.define(ClassTotal("S", 9980, "S"))


final_S = []

trace_rates = np.linspace(0.1, 1.9, 10)
avgs = []
for rate in trace_rates:
    print("starting rate: ", rate)
    avg = 0
    for _ in range(10):
        SIR.population.trace_rate = 1/rate
        data = SIR.run(list(range(200)))
        final_S = data["S"][-1]
        avg += final_S
    avgs.append(avg/100)
    print("finished rate: ", rate)

plt.plot(trace_rates, avgs)
plt.xlabel("trace rate")
plt.ylabel("average final susceptible population")
plt.show()

# plt.plot(data["time"], data["S"], color="red")
#plt.plot(data["time"], data["S"], color="blue")
#plt.show()
