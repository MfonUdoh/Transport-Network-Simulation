### Triler paths and loading ###

class Trailer(object):

    def __init__(self, origin, destination):
        self.name = 'Trailer{}:{}'.format(origin, destination)
        self.destination = destination
        self.origin = origin
        self.x = origin.x
        self.y = origin.y
        self.capacity = 5
        self.cargo = []
        self.dep_time = -1
        self.prev_time = -1

    def __str__(self):
        return self.name

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