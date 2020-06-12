### Triler paths and loading ###

class Trailer(object):

    def __init__(self, origin, destination):
        self.name = 'Trailer{}:{}'.format(origin, destination)
        self.state = "waiting"
        self.destination = destination
        self.origin = origin
        self.capacity = 5
        self.cargo = []
        self.dep_time = -1
        self.arr_time = 0
        self.load_count = 0
        self.load_time = 2
        self.unload_count = 0
        self.unload_time = 0
        self.wait_time = 0
        self.clock = 0

    def __str__(self):
        return self.name
    def define(self):
        return {'name':self.name,'state':self.state, 'origin':self.origin.name, 'destination':self.destination.name, 'dep_time':self.dep_time, 'arr_time':self.arr_time, 'cargo':len(self.cargo)}

    def travel(self, now):
        # Defining which course of action to take in 
        # if self.loading >= self.capacity:
        self.state = 'travel'
        self.dep_time = now

    def arrive(self, now):
        self.state = 'waiting'
        self.arr_time = now

    def full(self):
        if len(self.cargo) >= self.capacity:
            return True
        else:
            return False

    def empty(self):
        if len(self.cargo) <= 0:
            return True
        else:
            return False