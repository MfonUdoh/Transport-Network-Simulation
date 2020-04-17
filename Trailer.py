### Triler paths and loading ###

class Trailer(object):

    def __init__(self, name):
        self.name = name
        self.state = "wait"
        self.destination = ''
        self.origin = ''
        self.location = ''
        self.capacity = 100
        self.cargo = []
        self.dep_time = -1
        self.arr_time = 0

    def __str__(self):
        return self.name
    def define(self):
        return {'name':self.name,'state':self.state,'dep_time':self.dep_time, 'arr_time':self.arr_time, 'cargo':[str(x) for x in self.cargo]}

    def travel(self, now):
        # Defining which course of action to take in 
        # if self.loading >= self.capacity:
        self.state = 'travel'
        self.dep_time = now

    def arrive(self, now):
        self.state = 'wait'
        self.arr_time = now