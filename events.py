#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class contact_event: 
    def __init__(self, person, contacter):
        self.contacter = contacter
        self.person = person 

class self_event:
    def __init__(self, person, transition):
        self.person = person
        self.transition = transition
        
class trace_event:
    def __init__(self, person, contact):
        self.person = person
        self.contact = contact
    

