class Consignment():
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.path = []
        self.pathDistance = 0
        self.currentStop = origin
        self.nextStop = None
        self.delivered = False
    
    def __str__(self):
        return self.name

    def define(self):
        return {'name': self.name, 'destination':self.destination.name, 'delivered': self.delivered}

    def update_journey(self, here):
        # Updates current stop and next stop given the current location in the path
        hereIndex = self.path.index(here)
        self.currentStop = self.path[hereIndex]
        if self.currentStop != self.destination.name:
            self.nextStop = self.path[hereIndex+1]
        else:
            self.delivered = True