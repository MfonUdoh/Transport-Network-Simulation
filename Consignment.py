class Consignment():
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.delivered = False
    
    def __str__(self):
        return self.name

    def define(self):
        return {'name': self.name, 'destination':self.destination.name, 'delivered': self.delivered}