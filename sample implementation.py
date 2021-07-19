#!/usr/bin/env python
# coding: utf-8

# In[ ]:



def gen(i):
    li = [i for i in range(100)]
    li.remove(i)
    if i<20:
        return Agent("E", number = i, neighbours = li, quarantined = False)
    return Agent("S", number = i, neighbours = li, quarantined = False)

per_capita_contact_rate=10
trace_rate = 10
population = Population(100, gen, per_capita_contact_rate, trace_rate)


states = ["S", "E", "P", "I", "A", "R", "T"]
traced_states = ["T"]
quar_period = 14

SIR = Simulation(states, traced_states, population, quar_period)            




SIR.define(Inf_trans(from_state = "E", to_state = "A", 
          waiting_time = lambda: np.random.exponential(1/0.1)))
SIR.define(Inf_trans(from_state = "E", to_state = "P", 
          waiting_time = lambda: np.random.exponential(1/0.9)))
SIR.define(Inf_trans(from_state = "A", to_state = "R", 
          waiting_time = lambda: np.random.exponential(1/0.4)))
SIR.define(Inf_trans(from_state = "P", to_state = "I", 
          waiting_time = lambda: np.random.exponential(1/0.1)))
SIR.define(Inf_trans(from_state = "I", to_state = "R", 
          waiting_time = lambda: np.random.exponential(1/0.5)))
SIR.define(Inf_trans(from_state = "I", to_state = "T", 
          waiting_time = lambda: np.random.exponential(1/4)))


SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="E" ,contact_quar=False,chance=0.1))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="E" ,contact_quar=True,chance=0.01))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="A" ,contact_quar=False,chance=0.2))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="A" ,contact_quar=True,chance=0.02))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="P" ,contact_quar=False,chance=0.6))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="P" ,contact_quar=True,chance=0.06))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="I" ,contact_quar=False,chance=1))
SIR.define(Contact(from_state = "S",to_state = "E",contact_state ="I" ,contact_quar=True,chance=0.1))







SIR.define(Total("Eu",20,"E",False)) #E unquarantined
SIR.define(Total("Eq",0,"E",True)) #E quarantined
SIR.define(class_Total("T",0,"T"))
data = SIR.run(list(range(100)))

print("time: ", data["time"])
print("E unquarantined: ", data["Eu"])
print("E quarantined: ", data["Eq"])
print("Tested: ", data["T"])

